from sanic.exceptions import SanicException


class PasswordException(SanicException):
    status_code = 500


class GeneratePasswordHashException(PasswordException):
    pass


class CheckPasswordHashException(PasswordException):
    pass
