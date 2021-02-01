import datetime

from marshmallow import Schema, fields, post_load, pre_load

from api.base import ResponseDto


class ResponseModifyUserInfoDtoSchema(Schema):
    id = fields.Int(required=True)
    login = fields.Str(required=True)
    created_at = fields.Str(required=True)
    updated_at = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @pre_load
    @post_load
    def date_time_to_string(self, data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = self.date_time_to_iso(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = self.date_time_to_iso(datetime.datetime.utcnow())
        return data

    @staticmethod
    def date_time_to_iso(param):
        if isinstance(param, datetime.datetime):
            param = param.isoformat()
        return param


class ResponseModifyUserInfoDto(ResponseDto, ResponseModifyUserInfoDtoSchema):
    __schema__ = ResponseModifyUserInfoDtoSchema