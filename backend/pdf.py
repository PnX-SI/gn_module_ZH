import base64
from datetime import datetime as dt
from io import BytesIO
from itertools import groupby
from pathlib import Path

from flask import current_app, render_template
from geonature.utils.config import config
from weasyprint import HTML

try:
    from staticmap import Line, StaticMap
except ImportError:
    print("cannot import staticmap, map generation in pdf will be unavailable")

from .utils import get_file_path, get_main_picture_id


def get_main_picture(id_zh: int):
    id_media = get_main_picture_id(id_zh)
    if id_media:
        file_path: str = get_file_path(id_media)
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return "data:image/jpeg;base64," + encoded_string.decode()
    return None


def gen_map(coordinates, url_template=None):
    if url_template is None:
        url_template = "http://c.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
    protocol = "http"
    if not protocol in url_template:
        url_template = f"{protocol}:{url_template}"
    if coordinates:
        m = StaticMap(width=600, height=300, url_template=url_template)
        for coord in coordinates:
            poly = Line(coord, "blue", 4)
            m.add_line(poly)
        image = m.render()
        with BytesIO() as output:
            image.save(output, format="PNG", quality=100)
            contents = base64.b64encode(output.getvalue())
        return "data:image/jpeg;base64," + contents.decode()
    return None


def multi_to_polys(multi):
    polys = []
    for mul in multi:
        polys += mul
    return tuple(polys)


def get_layer(small_layer_nb=0, area=None, threshold=None):
    """
    Returns the correct layer depending on the threshold
    """
    base_map_from_config = config.get("MAPCONFIG", {}).get("BASEMAP", [{}])
    # The replace here is because Static map does not support url constructed with {s}
    # The {s} is for server (generally replace by a,b and c). So need to replace it by hand
    # Cannot use .format() since it is only partial (z,x,y are not formatted)
    # Work only with layers
    base_map = (
        lambda nb: base_map_from_config[nb]
        .get("url", "http//c.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png")
        .replace("{s}", "c")
    )

    if area is None:
        return base_map(0)
    if threshold is None:
        return base_map(0)
    if area < threshold:
        return base_map(small_layer_nb)
    return base_map(0)


def gen_pdf(id_zh, dataset, filename="rapport.pdf"):
    coordinates = dataset.get("geometry", {}).get("coordinates", [[]])
    poly_type = dataset.get("geometry", {}).get("type", "")
    if poly_type is not None:
        if poly_type == "Polygon":
            coordinates = coordinates
        else:
            coordinates = multi_to_polys(coordinates)
    try:
        # For now, the url_template cannot be taken from the config since
        # StaticMap does not support urls like :
        # {s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png with the "{s}"
        area = float(dataset["description"]["presentation"]["area"])
        threshold = dataset["config"]["pdf_layer_threashold_ha"]
        layer_nb = dataset["config"]["pdf_layer_number"]
        layer = get_layer(small_layer_nb=layer_nb, area=area, threshold=threshold)
        dataset["map"] = gen_map(coordinates, url_template=layer)
    except Exception as e:
        print(f"Cannot generate the map inside the pdf ({e})... Continuing")

    try:
        dataset["image"] = get_main_picture(id_zh=id_zh)
    except Exception as e:
        print("Cannot find image")

    # Pre-treatment of other inventories:
    others = {}
    for k, v in groupby(dataset["statuts"]["autre_inventaire"], key=lambda x: x["zh_type_name"]):
        others[k] = list(v)
    dataset["statuts"]["autres_inventaires"] = others

    #  pdf date
    dataset["date_now"] = dt.now().strftime("%d/%m/%Y - %H:%M:%S")

    # Generate pdf
    pdf_file = generate_pdf_from_template("fiche_template_pdf.html", dataset, filename)
    return Path(pdf_file)


@current_app.template_filter("datetime_format")
def datetime_format(value: str, format="%d-%m-%y"):
    date = dt.strptime(value, "%Y-%m-%d %H:%M:%S")
    return date.strftime(format)


def generate_pdf_from_template(template, data, filename):
    template_rendered = render_template(template, data=data)
    html_file = HTML(
        string=template_rendered, base_url=current_app.config["API_ENDPOINT"], encoding="utf-8"
    )
    html_file.write_pdf(filename)
    return filename
