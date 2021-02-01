from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.message.create import RequestCreateMessageDto
from api.responses.message.message_info import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException
from db.queries.message import create_message, get_user_messages
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException


# method_post: create message
# method_get : return list messages
class MessageEndpoint(BaseEndpoint):
    async def method_post(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)

        try:
            db_message = create_message(session, request_model, token.get('user_id'))
        except DBUserNotExistsException:
            raise SanicUserNotFoundException(message='Recipient not found')
        else:
            session.commit_session()

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        user_id = token.get('user_id')
        try:
            messages = get_user_messages(session, user_id)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException(message='User not exists')

        response_model = ResponseMessageDto(messages, many=True)
        return await self.make_response_json(body=response_model.dump(), status=200)