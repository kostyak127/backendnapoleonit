from sanic.exceptions import SanicException


class SanicUserExistsException(SanicException):
    status_code = 409


class SanicUserNotFoundException(SanicException):
    status_code = 404
    message = 'User not found'


class SanicPasswordException(SanicException):
    status_code = 500


class SanicAuthException(SanicException):
    status_code = 401


class SanicMessageNotFoundException(SanicException):
    status_code = 404
    message = 'message not found'