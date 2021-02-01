from marshmallow import Schema, fields
from sanic.exceptions import SanicException

from api.base import ResponseDto


class ValidationError(SanicException):
    status_code = 400


"""class ResponseAuthUserDtoSchema(Schema):
    def __init__(self, *args, **kwargs):
        self.fields = {'Authorization': ''}

    def load(self, data: dict):
        valid_data = dict()

        for key, value in data.items():
            if key not in self.fields:
                continue
            if not isinstance(value, self.fields[key].__class__):
                raise ValidationError(f'{key} should be str')

            valid_data[key] = value

        return valid_data
"""


class ResponseAuthUserDtoSchema(Schema):
    Authorization = fields.Str(required=True)


class ResponseAuthUserDto(ResponseDto, ResponseAuthUserDtoSchema):
    __schema__ = ResponseAuthUserDtoSchema


class AuthUserResponseObject:
    def __init__(self, token):
        self.Authorization = token