import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResponseDto


class ResponseMessageDtoSchema(Schema):
    id = fields.Int(required=True, allow_none=False)
    sender_id = fields.Int(required=True, allow_none=False)
    recipient_id = fields.Int(required=True, allow_none=False)
    created_at = fields.Str(required=True, allow_none=False)
    updated_at = fields.Str(required=True, allow_none=False)
    message = fields.Str(required=True, allow_none=False)

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


class ResponseMessageDto(ResponseDto, ResponseMessageDtoSchema):
    __schema__ = ResponseMessageDtoSchema
