import pdb

from werkzeug.utils import secure_filename

from pathlib import Path

import os

from geonature.utils.env import ROOT_DIR

from .utils import get_file_path


def upload(request, extensions, pdf_size, jpg_size, upload_path, module_name):
    try:
        # to do : set file name : file_name_1, _2, ... for main_picture

        # get form data
        metadata = request.form.to_dict()

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

        media_path = Path(
            'external_modules', module_name, upload_path, filename)
        full_path = ROOT_DIR / media_path

        # check user file extension (changer)
        extension = Path(full_path).suffix.lower()
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

        # save user file in upload directory
        file.save(full_path)

        if not os.path.isfile(full_path):
            return {"error": "ERROR_WHILE_LOADING_FILE"}

        return {
            "file_name": filename,
            "full_path": str(full_path),
            "media_path": str(media_path),
            "extension": extension,
        }
    except Exception:
        raise
