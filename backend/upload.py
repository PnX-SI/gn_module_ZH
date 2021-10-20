import pdb

from werkzeug.utils import secure_filename

from pathlib import Path

import os


def upload(id_zh, request, extensions, pdf_size, jpg_size, upload_path):
    try:
        # to do : set file name : file_name_1, _2, ...

        if "File" not in request.files:
            return {"error": "NO_FILE_SENDED"}

        file = request.files["File"]

        if file.filename == "":
            return {"error": "NO_FILE_SENDED"}

        # get file path
        filename = filename = secure_filename(file.filename)
        filename = secure_filename(filename)
        if len(filename) > 100:
            return {"error": "FILE_NAME_TOO_LONG"}

        base_path = Path(__file__).absolute().parent
        full_path = os.path.join(base_path, upload_path, filename)

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
            "full_path": full_path,
            "is_uploaded": True,
            "extension": extension,
        }
    except Exception:
        raise
