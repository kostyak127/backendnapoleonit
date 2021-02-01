from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.message.modify import RequestModifyMessageDto
from api.responses.message.message_info import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBMessageNotExistsException, DBUserNotExistsException
from db.queries.message import get_message, modify_message, delete_message
from db.queries.user import get_user
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicMessageNotFoundException, SanicUserNotFoundException


# method get: return message by id
# method patch: modify message by id
# method delete: delete message by id
class MessageInfoEndpoint(BaseEndpoint):
    async def method_get(
            self, request: Request, body: dict, session: DBSession, token: dict, message_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_user_id = token.get('user_id')

        try:
            get_user(session, user_id=request_user_id)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException

        try:
            db_message = get_message(session, message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFoundException

        if db_message.sender_id != request_user_id:
            return await self.make_response_json(status=403)

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=200)

    async def method_patch(
        self, request: Request, body: dict, session: DBSession, token: dict, message_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_model = RequestModifyMessageDto(data=body)
        request_user_id = token.get('user_id')

        try:
            db_user = get_user(session, user_id=request_user_id)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException

        try:
            db_message = modify_message(session, message_id, request_model.message)
        except DBMessageNotExistsException:
            raise SanicMessageNotFoundException

        if db_message.sender_id != db_user.id:
            return await self.make_response_json(status=403)
        else:
            session.commit_session()

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(response_model.dump(), status=200)

    async def method_delete(
        self, request: Request, body: dict, session: DBSession, token: dict, message_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        request_user_id = token.get('user_id')

        try:
            db_user = get_user(session, user_id=request_user_id)
        except DBUserNotExistsException:
            raise SanicUserNotFoundException

        try:
            db_message = delete_message(session, message_id)
        except DBMessageNotExistsException:
            raise SanicMessageNotFoundException

        if db_message.sender_id != db_user.id:
            return await self.make_response_json(status=403)
        else:
            session.commit_session()

        return await self.make_response_json(status=200)