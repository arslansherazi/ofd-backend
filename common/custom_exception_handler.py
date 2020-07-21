from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code

    def __str__(self):
        return str(self.detail)
