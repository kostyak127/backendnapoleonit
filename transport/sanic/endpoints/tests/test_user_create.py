import pytest

from transport.sanic.endpoints import CreateUserEndpoint
from transport.sanic.exceptions import SanicUserExistsException


@pytest.mark.asyncio
async def test_create_user_if_user_exists(patched_context, valid_request_body, request_factory, mocker,
                                          valid_user, config_test):
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('db.database.DBSession.get_user_by_login', return_value=valid_user)

    request = request_factory(method='post',)
    endpoint = CreateUserEndpoint(config_test, patched_context, '', ())

    with pytest.raises(SanicUserExistsException):
        await endpoint(request)


@pytest.mark.asyncio
async def test_create_user_correct(patched_context, valid_request_body, request_factory, mocker,
                                   valid_user, config_test, session):
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.endpoints.users.create.create_user', return_value=valid_user)
    mocker.patch('db.database.Database.make_session', return_value=session())

    request = request_factory(method='post')
    endpoint = CreateUserEndpoint(config_test, patched_context, '', ())
    response = await endpoint(request)
    assert response.status == 201