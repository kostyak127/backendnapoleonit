from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request.create_user import RequestCreateUserDto
from api.responses.user import ResponseUserDto
from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException, UserExistsException
from transport.sanic.endpoints import BaseEndpoint

from db.queries import user as users_queries


class CreateUserEndpoint(BaseEndpoint):
    async def method_post(self, request: Request, body: dict, session: DBSession, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        try:
            db_user = users_queries.create_user(session, request_model)
            session.commit_session()
        except UserExistsException:
            return await self.make_response_json(status=409, message='User already exists')
        except (DBDataException, DBIntegrityException) as error:
            return await self.make_response_json(status=500, message=str(error))

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(status=201, body=response_model.dump())
