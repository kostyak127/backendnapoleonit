from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.user.auth import RequestAuthUserDto
from api.responses.user.auth import AuthUserResponseObject, ResponseAuthUserDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException
from db.queries.user import check_user_exists, get_user
from helpers.password.exception import CheckPasswordHashException
from helpers.password.hash import check_hash
from helpers.token.token import create_token
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException, SanicPasswordException


class AuthUserEndpoint(BaseEndpoint):
    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestAuthUserDto(data=body)

        db_user = get_user(session, login=request_model.login)
        try:
            check_user_exists(db_user)
        except DBUserNotExistsException as e:
            raise SanicUserNotFoundException(message=e.message)

        try:
            if not check_hash(request_model.password, db_user.password):
                raise CheckPasswordHashException
        except CheckPasswordHashException:
            raise SanicPasswordException('wrong password')

        payload = {
            'user_id': db_user.id
        }

        token = create_token(payload, self.config.token.secret)

        response = AuthUserResponseObject(token)
        response_model = ResponseAuthUserDto(response)

        return await self.make_response_json(status=200, body=response_model.dump())