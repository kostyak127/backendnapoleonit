from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseDeleteUserDtoSchema(Schema):
    id = fields.Int(required=True)
    login = fields.Str(required=True)
    is_delete = fields.Bool(required=True)


class ResponseDeleteUserDto(ResponseDto, ResponseDeleteUserDtoSchema):
    __schema__ = ResponseDeleteUserDtoSchema
