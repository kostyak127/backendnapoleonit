class DBIntegrityException(Exception):
    pass


class DBDataException(Exception):
    pass


class DBUserExistsException(DBDataException):
    message = 'User already exists'


class DBUserNotExistsException(DBDataException):
    message = 'User not found'


class DBMessageNotExistsException(DBDataException):
    message = 'Message not found'
