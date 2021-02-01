from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.exceptions import ValidationException
from transport.sanic.base import SanicEndpoint


class BaseEndpoint(SanicEndpoint):
    async def method_(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:

        database = self.context.database

        session = database.make_session()
        try:
            return await super().method_(request, body, session, *args, **kwargs)
        except ValidationException as error:
            return await self.make_response_json(status=error.status_code, message=str(error))