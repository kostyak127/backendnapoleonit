import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResponseDto


class ResponseGetUserInfoDtoSchema(Schema):
    login = fields.Str(required=True)
    id = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @pre_load
    @post_load
    def date_time_to_string(self, data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = self.date_time_to_iso(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = self.date_time_to_iso(data['updated_at'])
        return data

    @staticmethod
    def date_time_to_iso(param):
        if isinstance(param, datetime.datetime):
            param = param.isoformat()
        return param


class ResponseGetUserInfoDto(ResponseDto, ResponseGetUserInfoDtoSchema):
    __schema__ = ResponseGetUserInfoDtoSchema
