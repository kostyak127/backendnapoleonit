from marshmallow import Schema, fields

from api.base import RequestDto


class RequestModifyUserInfoDtoSchema(Schema):
    first_name = fields.Str(allow_none=False)
    last_name = fields.Str(allow_none=False)


class RequestModifyUserInfoDto(RequestDto, RequestModifyUserInfoDtoSchema):
    __schema__ = RequestModifyUserInfoDtoSchema

    def __init__(self, *args, **kwargs):
        self.fields = []
        super(RequestModifyUserInfoDto, self).__init__(*args, **kwargs)

    def set(self, key, value):
        self.fields.append(key)
        super(RequestModifyUserInfoDto, self).set(key, value)