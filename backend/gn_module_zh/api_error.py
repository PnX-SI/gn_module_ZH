from werkzeug.exceptions import InternalServerError


class ZHApiError(InternalServerError):
    def __init__(self, message, details="", status_code=None):
        description = message
        if details:
            description += " - " + details
        super().__init__(description=description)
        if status_code is not None:
            self.code = status_code
