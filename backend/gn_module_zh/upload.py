import os
import sys
from pathlib import Path

from geonature.core.gn_commons.models import TMedias
from geonature.utils.env import DB, ROOT_DIR
from sqlalchemy.sql import update, select
from werkzeug.utils import secure_filename

from .api_error import ZHApiError
from .forms import patch_file_info, post_file_info, update_file_extension
from .utils import get_extension, get_file_path


def upload_process(
    request, extensions, pdf_size, jpg_size, upload_path, module_name, id_media=None
):
    if request.files:
        check_file_name(request)

        if id_media:
            try:
                os.remove(get_file_path(id_media))
            except:
                pass

    # upoad file - including post to t_medias
    upload_file = upload(
        request, extensions, pdf_size, jpg_size, upload_path, module_name, id_media
    )

    # checks if error in user file or user http request:
    if "error" in upload_file:
        raise ZHApiError(
            message=upload_file["error"], details=upload_file["error"], status_code=400
        )

    return {
        "media_path": upload_file["media_path"],
        "secured_file_name": upload_file["file_name"],
        "id_media": id_media,
    }


def upload(request, extensions, pdf_size, jpg_size, upload_path, module_name, id_media):
    if request.files:
        # get file
        file = request.files["file"]

        # get file path
        filename = secure_filename(file.filename)
        filename = secure_filename(filename)
        if len(filename) > 100:
            return {"error": "FILE_NAME_TOO_LONG"}

        # check user file extension (changer)
        extension = get_extension(filename)
        if extension not in extensions:
            return {"error": "FILE_EXTENSION_ERROR"}

        # check file size
        file.seek(0, 2)
        size = file.tell() / (1024 * 1024)
        file.seek(0)

        if extension == ".pdf" and (size > pdf_size):
            return {"error": "FILE_OVERSIZE"}
        if extension == ".jpg" and (size > jpg_size):
            return {"error": "FILE_OVERSIZE"}

    # post/patch here upload info to t_medias in order to include id_media as a prefix for filename (unique name)
    summary = request.form.to_dict()["summary"]
    summary = summary if summary != "null" else None
    if id_media:
        patch_file_info(
            request.form.to_dict()["id_zh"],
            id_media,
            request.form.to_dict()["title"],
            request.form.to_dict()["author"],
            summary,
        )
    else:
        # save in db
        id_media = post_file_info(
            request.form.to_dict()["id_zh"],
            request.form.to_dict()["title"],
            request.form.to_dict()["author"],
            summary,
            extension,
        )

    if request.files:
        # set file name
        media_filename = "_".join([str(id_media), filename])
        media_path = Path("external_modules", module_name, upload_path, media_filename)
        full_path = ROOT_DIR / media_path

        # save user file in upload directory
        file.save(full_path)

        if not os.path.isfile(full_path):
            return {"error": "ERROR_WHILE_LOADING_FILE"}

        # update TMedias.media_path with media_filename
        DB.session.execute(
            update(TMedias).where(TMedias.id_media == id_media).values(media_path=str(media_path))
        )

        update_file_extension(id_media, extension)

    DB.session.flush()

    return {
        "file_name": get_file_path(id_media).name,
        "full_path": str(get_file_path(id_media)),
        "media_path": DB.session.execute(select(TMedias.media_path).where(TMedias.id_media == id_media)).scalar_one(),
        "extension": get_extension(get_file_path(id_media).name),
    }


def check_file_name(request):
    try:
        if "file" not in request.files:
            return {"error": "NO_FILE_SENDED"}
        else:
            if request.files["file"].filename == "":
                return {"error": "NO_FILE_SENDED"}
        file_name = secure_filename(request.files["file"].filename)
        temp = file_name.split(".")
        extension = temp[len(temp) - 1]
    except Exception:
        file_name = "Filename_error"
        extension = "Extension_error"
        raise
