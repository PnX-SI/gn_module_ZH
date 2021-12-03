from pathlib import Path
from io import BytesIO
import base64
try:
    from staticmap import StaticMap, Line
except ImportError:
    print('cannot import staticmap, map generation in pdf will be unavailable')

# Filemanager
import geonature.utils.filemanager as fm

from .utils import get_main_picture_id, get_file_path


def get_main_picture(id_zh: int):
    id_media = get_main_picture_id(id_zh)
    if id_media:
        return get_file_path(id_media)
    return None


def gen_map(coordinates):
    if coordinates:
        m = StaticMap(width=600, height=300)
        for coord in coordinates:
            poly = Line(coord, 'blue', 4)
            m.add_line(poly)
        image = m.render()
        with BytesIO() as output:
            image.save(output, format='PNG')
            contents =  base64.b64encode(output.getvalue())
        return "data:image/jpeg;base64," + contents.decode()
    return None


def multi_to_polys(multi):
    polys = []
    for mul in multi:
        polys += mul
    return tuple(polys)


def gen_pdf(id_zh, dataset, filename = "rapport.pdf"):
    coordinates = dataset.get('geometry', {}).get('coordinates', [[]])
    poly_type = dataset.get('geometry', {}).get('type', '')
    if poly_type is not None:
        if poly_type == 'Polygon':
            coordinates = coordinates
        else:
            coordinates = multi_to_polys(coordinates)
    try:
        dataset['map'] = gen_map(coordinates)
    except Exception as e:
        print('Cannot generate the map inside the pdf... Continuing')
    
    try:
        dataset['image'] = get_main_picture(id_zh=id_zh)
    except Exception as e:
        print('Cannot find image')

    pdf_file = fm.generate_pdf("fiche_template_pdf.html", dataset, filename)
    return Path(pdf_file)
  