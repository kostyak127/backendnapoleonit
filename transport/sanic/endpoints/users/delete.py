from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.responses.user.delete import ResponseDeleteUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException
from db.queries.user import delete_user
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException


class DeleteUserEndpoint(BaseEndpoint):
    async def method_delete(
        self, request: Request, body: dict, session: DBSession, token: dict, user_id: int, *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('user_id') != user_id:
            return await self.make_response_json(status=403)

        try:
            db_user = delete_user(session, user_id)
            session.commit_session()
        except DBUserNotExistsException as e:
            raise SanicUserNotFoundException(message=e.message)

        response_model = ResponseDeleteUserDto(db_user)
        return await self.make_response_json(body=response_model.dump(), status=200)