from marshmallow import Schema, fields

from api.base import RequestDto


class RequestCreateEmployeeDtoSchema(Schema):
    firstname = fields.Str(required=True, allow_none=True)
    lastname = fields.Str(required=True, allow_none=True)


class RequestCreateEmployeeDto(RequestDto, RequestCreateEmployeeDtoSchema):
    __schema__ = RequestCreateEmployeeDtoSchema