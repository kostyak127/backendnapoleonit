from marshmallow import Schema, fields

from api.base import RequestDto


class RequestModifyMessageDtoSchema(Schema):
    message = fields.Str(required=True, allow_none=False)


class RequestModifyMessageDto(RequestDto, RequestModifyMessageDtoSchema):
    __schema__ = RequestModifyMessageDtoSchema