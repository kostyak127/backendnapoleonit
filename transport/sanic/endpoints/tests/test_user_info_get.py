import pytest

from transport.sanic.endpoints import InfoUserEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException


@pytest.mark.asyncio
async def test_info_user_get_if_wrong_id(patched_context, valid_request_body, request_factory, mocker,
                                         config_test):
    user_id = 1
    wrong_user_id = 2
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})

    request = request_factory(method='get')
    endpoint = InfoUserEndpoint(config_test, patched_context, '', (), True)

    response = await endpoint(request, user_id=wrong_user_id)

    assert response.status == 403


@pytest.mark.asyncio
async def test_info_user_get_if_user_not_exists(patched_context, valid_request_body, request_factory, mocker,
                                                config_test):
    user_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.users.info.get_user', return_value=None)

    request = request_factory(method='get')
    endpoint = InfoUserEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request, user_id=user_id)


@pytest.mark.asyncio
async def test_info_user_get_if_user_is_delete(patched_context, valid_request_body, request_factory, mocker,
                                               config_test, deleted_valid_user):
    user_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.users.info.get_user', return_value=deleted_valid_user)

    request = request_factory(method='get')
    endpoint = InfoUserEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request, user_id=user_id)


@pytest.mark.asyncio
async def test_info_user_get_correct_work(patched_context, valid_request_body, request_factory, mocker,
                                          config_test, valid_user):
    user_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.users.info.get_user', return_value=valid_user)

    request = request_factory(method='get')
    endpoint = InfoUserEndpoint(config_test, patched_context, '', (), True)
    response = await endpoint(request, user_id=user_id)

    assert response.status == 200
