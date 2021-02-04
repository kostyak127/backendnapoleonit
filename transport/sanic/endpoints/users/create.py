from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.user.create import RequestCreateUserDto
from api.responses.user.create import ResponseCreateUserDto
from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException, DBUserExistsException
from helpers.password.hash import generate_password
from transport.sanic.endpoints import BaseEndpoint

from db.queries import create_user
from transport.sanic.exceptions import SanicUserExistsException


class CreateUserEndpoint(BaseEndpoint):
    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(data=body)  # API

        hashed_password = generate_password(request_model.password)

        try:
            db_user = create_user(session, request_model, hashed_password)  # DB
            session.commit_session()
        except DBUserExistsException as e:
            raise SanicUserExistsException(message=e.message)
        except (DBDataException, DBIntegrityException) as error:
            return await self.make_response_json(status=500, message=str(error))

        response_model = ResponseCreateUserDto(db_user)  # API

        return await self.make_response_json(status=201, body=response_model.dump())