class GeneratePasswordHashException(Exception):
    status_code = 500
    message = 'Can`t generate password'


class CheckPasswordHashException(Exception):
    status_code = 403
    message = 'Wrong password'