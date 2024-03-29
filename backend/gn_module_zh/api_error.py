class ZHApiError(Exception):
    status_code = 500

    def __init__(self, message, details="", status_code=None):
        Exception.__init__(self)
        self.message = message
        self.details = details
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            "message": self.message,
            "details": self.details,
            "raisedError": self.__class__.__name__,
        }

    def __str__(self):
        return self.message
