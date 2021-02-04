from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.message.create import RequestCreateMessageDto
from api.responses.message.message_info import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException
from db.queries import get_user
from db.queries.message import create_message, get_user_messages
from db.queries.user import check_user_exists
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException


# method_post: create message
# method_get : return list messages
class MessageEndpoint(BaseEndpoint):
    async def method_post(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        request_model = RequestCreateMessageDto(body)
        sender_id = token.get('user_id')
        db_sender = get_user(session, user_id=sender_id)
        recipient_login = request_model.recipient
        db_recipient = get_user(session, login=recipient_login)

        try:
            check_user_exists(db_sender)
            check_user_exists(db_recipient)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException(message='Recipient or Sender not found')
        else:
            db_message = create_message(session, request_model, sender_id)
            session.commit_session()

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        sender_id = token.get('user_id')
        db_sender = get_user(session, user_id=sender_id)
        try:
            check_user_exists(db_sender)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException(message='User not exists')
        else:
            messages = get_user_messages(session, sender_id)

        response_model = ResponseMessageDto(messages, many=True)
        return await self.make_response_json(body=response_model.dump(), status=200)