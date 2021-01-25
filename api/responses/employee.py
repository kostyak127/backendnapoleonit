import datetime

from marshmallow import Schema, fields, pre_load, post_load

from api.base import ResponseDto


class ResponseEmployeeDtoSchema(Schema):
    id = fields.Int(required=True, allow_none=False)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)

    @pre_load
    @post_load
    def deserialize_datetime(self, data: dict, **kwargs) -> dict:
        if 'created_at' in data:
            data['created_at'] = self.datetime_to_iso(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = self.datetime_to_iso(data['updated_at'])

        return data

    @staticmethod
    def datetime_to_iso(dt):
        if isinstance(dt, datetime.datetime):
            return dt.isoformat()
        return dt


class ResponseEmployeeDto(ResponseDto, ResponseEmployeeDtoSchema):
    __schema__ = ResponseEmployeeDtoSchema
