from marshmallow import Schema, ValidationError, EXCLUDE

from api.exceptions import ApiValidationException, ApiResponseValidationException


class RequestDto:
    __schema__: Schema

    def __init__(self, data: dict):
        try:
            valid_data = self.__schema__(unknown=EXCLUDE).load(data)
        except ValidationError as error:
            raise ApiValidationException(error.messages)
        else:
            self._import(valid_data)

    def _import(self, data: dict):
        for name, field in data.items():
            self.set(name, field)

    def set(self, key, value):
        setattr(self, key, value)


class ResponseDto:
    __schema__: Schema

    def __init__(self, obj: object):
        properties = {}
        for prop in dir(obj):
            if not prop.startswith('_') and not prop.endswith('_'):
                attr = getattr(obj, prop)
                try:
                    if not callable(attr):
                        properties[prop] = attr
                except Exception as e:
                    print(e.__class__)
                    continue

        try:
            self._data = self.__schema__(unknown=EXCLUDE).load(properties)
        except ValidationError as error:
            raise ApiResponseValidationException(error.messages)

    def dump(self) -> dict:
        return self._data
