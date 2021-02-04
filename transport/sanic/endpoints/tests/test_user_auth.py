import pytest

from transport.sanic.endpoints import AuthUserEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException, SanicPasswordException


@pytest.mark.asyncio
async def test_auth_user_if_not_exits(patched_context, valid_request_body, request_factory, mocker):
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.endpoints.users.auth.get_user', return_value=None)
    request = request_factory(method='post')
    endpoint = AuthUserEndpoint(None, patched_context, '', ())

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request)


@pytest.mark.asyncio
async def test_auth_user_if_user_is_delete(patched_context, valid_request_body, request_factory, mocker,
                                           deleted_valid_user):
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.endpoints.users.auth.get_user', return_value=deleted_valid_user)

    request = request_factory(method='post')
    endpoint = AuthUserEndpoint(None, patched_context, '', ())

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request)


@pytest.mark.asyncio
async def test_auth_user_if_wrong_password(patched_context, valid_request_body, request_factory, mocker, valid_user):
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.endpoints.users.auth.get_user', return_value=valid_user)
    mocker.patch('transport.sanic.endpoints.users.auth.check_hash', return_value=False)

    request = request_factory(method='post')
    endpoint = AuthUserEndpoint(None, patched_context, '', ())

    with pytest.raises(SanicPasswordException):
        await endpoint(request)


@pytest.mark.asyncio
async def test_auth_user_correct_work(patched_context, valid_request_body, request_factory, mocker,
                                      valid_user, config_test):
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.endpoints.users.auth.get_user', return_value=valid_user)
    mocker.patch('transport.sanic.endpoints.users.auth.check_hash', return_value=True)
    mocker.patch('transport.sanic.endpoints.users.auth.create_token', return_value='CORRECT_TOKEN')

    request = request_factory(method='post')
    endpoint = AuthUserEndpoint(config_test, patched_context, '', ())
    response = await endpoint(request)
    assert response.status == 200