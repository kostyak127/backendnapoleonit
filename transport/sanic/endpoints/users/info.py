from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.user.modify_info import RequestModifyUserInfoDto
from api.responses.user.get_info import ResponseGetUserInfoDto
from api.responses.user.modify_info import ResponseModifyUserInfoDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException
from db.queries.user import get_user, modify_user, check_user_exists
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException


class InfoUserEndpoint(BaseEndpoint):
    async def method_get(
        self, request: Request, body: dict, session: DBSession, user_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('user_id') != user_id:
            return await self.make_response_json(status=403, message='Token not right')

        db_user = get_user(session, user_id=user_id)
        try:
            check_user_exists(db_user)
        except DBUserNotExistsException as e:
            raise SanicUserNotFoundException(message=e.message)

        response_model = ResponseGetUserInfoDto(db_user)

        return await self.make_response_json(body=response_model.dump(), status=200)

    async def method_patch(
        self, request: Request, body: dict, session: DBSession, user_id: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:

        if token.get('user_id') != user_id:
            return await self.make_response_json(status=403)

        request_model = RequestModifyUserInfoDto(data=body)

        db_user = get_user(session, user_id=user_id)
        try:
            check_user_exists(db_user)
        except DBUserNotExistsException as e:
            raise SanicUserNotFoundException(message=e.message)
        else:
            modified_user = modify_user(session, user_id=user_id, to_modify=request_model)
            session.commit_session()

        response_model = ResponseModifyUserInfoDto(modified_user)
        return await self.make_response_json(body=response_model.dump(), status=200)