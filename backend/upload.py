import pdb
import sys

from werkzeug.utils import secure_filename
from pathlib import Path
import os

from geonature.utils.env import ROOT_DIR
from geonature.utils.env import DB
from geonature.core.gn_commons.models import TMedias

from .utils import get_file_path
from .api_error import ZHApiError
from .forms import post_file_info, patch_file_info


def upload_process(request, extensions, pdf_size, jpg_size, upload_path, module_name, id_media=None):

    check_file_name(request.files["file"])

    if id_media:
        try:
            os.remove(get_file_path(id_media))
        except:
            pass

    # upoad file - including post to t_medias
    upload_file = upload(
        request,
        extensions,
        pdf_size,
        jpg_size,
        upload_path,
        module_name,
        id_media
    )

    # checks if error in user file or user http request:
    if "error" in upload_file:
        raise ZHApiError(
            message=upload_file["error"], details=upload_file["error"], status_code=400)

    return {
        "media_path": upload_file["media_path"],
        "secured_file_name": upload_file['file_name'],
        "original_file_name": request.files["file"].filename,
        "id_media": id_media
    }


def upload(request, extensions, pdf_size, jpg_size, upload_path, module_name, id_media):
    try:
        if "file" not in request.files:
            return {"error": "NO_FILE_SENDED"}

        file = request.files["file"]

        if file.filename == "":
            return {"error": "NO_FILE_SENDED"}

        # get file path
        filename = secure_filename(file.filename)
        filename = secure_filename(filename)
        if len(filename) > 100:
            return {"error": "FILE_NAME_TOO_LONG"}

        # check user file extension (changer)
        split_filename = filename.split('.')
        extension = '.' + split_filename[len(split_filename)-1]
        if extension not in extensions:
            return {"error": "FILE_EXTENSION_ERROR"}

        # check file size
        file.seek(0, 2)
        size = file.tell() / (1024 * 1024)
        file.seek(0)

        if extension == '.pdf' and (size > pdf_size):
            return {"error": "FILE_OVERSIZE"}
        if extension == '.jpg' and (size > jpg_size):
            return {"error": "FILE_OVERSIZE"}

        # post/patch here upload info to t_medias in order to include id_media as a prefix for filename (unique name)
        if id_media:
            patch_file_info(
                request.form.to_dict()['id_zh'],
                id_media,
                request.form.to_dict()['title'],
                request.form.to_dict()['author'],
                request.form.to_dict()['summary'],
                extension
            )
        else:
            # save in db
            id_media = post_file_info(
                request.form.to_dict()['id_zh'],
                request.form.to_dict()['title'],
                request.form.to_dict()['author'],
                request.form.to_dict()['summary'],
                extension
            )

        media_filename = '_'.join([str(id_media), filename])
        media_path = Path(
            'external_modules', module_name, upload_path, media_filename)
        full_path = ROOT_DIR / media_path

        # save user file in upload directory
        file.save(full_path)

        if not os.path.isfile(full_path):
            return {"error": "ERROR_WHILE_LOADING_FILE"}

        # update TMedias.media_path with media_filename
        DB.session.query(TMedias).filter(TMedias.id_media ==
                                         id_media).update({'media_path': str(media_path)})
        DB.session.flush()

        return {
            "file_name": filename,
            "full_path": str(full_path),
            "media_path": str(media_path),
            "extension": extension,
        }
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        raise ZHApiError(
            message="upload_error", details=str(exc_type) + ': ' + str(e.with_traceback(tb)))


def check_file_name(file):
    try:
        file_name = secure_filename(file.filename)
        temp = file_name.split(".")
        extension = temp[len(temp) - 1]
    except Exception as e:
        file_name = "Filename_error"
        extension = "Extension_error"
        raise
