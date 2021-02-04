from http import HTTPStatus

from sanic.request import Request
from sanic.response import BaseHTTPResponse, json

from configs.config import ApplicationConfig

from typing import Iterable

from context import Context
from helpers.token.exceptions import ReadTokenException
from helpers.token.token import read_token
from transport.sanic.exceptions import SanicAuthException


class SanicEndpoint:
    async def __call__(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:

        if self.need_auth:
            try:
                token = {'token': self.import_body_auth(request, self.config.token.secret)}
            except SanicAuthException as error:
                return await self.make_response_json(status=error.status_code)
            else:
                kwargs.update(token)

        return await self.handle_request(request, *args, **kwargs)

    def __init__(self,
                 config: ApplicationConfig,
                 context: Context,
                 uri: str,
                 methods: Iterable,
                 need_auth: bool = False,
                 *args, **kwargs):
        self.config = config
        self.context = context
        self.uri = uri
        self.methods = methods
        self.need_auth = need_auth
        self.__name__ = self.__class__.__name__

    @staticmethod
    async def make_response_json(body: dict = None,
                                 status: int = 200,
                                 message: str = None,
                                 error_code: int = None) -> BaseHTTPResponse:
        if body is None:
            body = {
                'message': message or HTTPStatus(status).phrase,
                'error_code': error_code or status
            }
        return json(body=body, status=status)

    @staticmethod
    def get_request_body(request: Request) -> dict:  # Преобразование json-объекта в словарь
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return dict()

    @staticmethod
    def get_request_headers(request: Request) -> dict:
        return {
            header: value
            for header, value in request.headers.items()
            if header.lower().startswith('x-')
        }

    @staticmethod
    def import_body_auth(request: Request, secret: str) -> dict:
        token = request.headers.get('Authorization')
        try:
            return read_token(token, secret)
        except ReadTokenException as error:
            raise SanicAuthException(str(error))

    async def handle_request(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        body = dict()

        body.update(self.get_request_body(request))
        body.update(self.get_request_headers(request))

        return await self.method_(request, body, *args, **kwargs)

    async def method_(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        method = request.method.lower()
        func_name = f'method_{method}'
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return await func(request, body, *args, **kwargs)
        else:
            return await self.method_not_implemented(method=method)

    # Base Methods

    async def method_not_implemented(self, method: str):
        return await self.make_response_json(status=500, message=f'Method {method} not implemented')

    async def method_get(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='GET')

    async def method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='POST')

    async def method_patch(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='PATCH')

    async def method_delete(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_implemented(method='DELETE')