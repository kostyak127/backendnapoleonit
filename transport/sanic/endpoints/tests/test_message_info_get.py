import pytest

from transport.sanic.endpoints import MessageInfoEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException, SanicMessageNotFoundException


@pytest.mark.asyncio
async def test_info_message_get_if_sender_not_exists(patched_context, valid_request_body, request_factory,
                                                     mocker,
                                                     config_test):
    user_id = 1
    message_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.messages.info.get_user', return_value=None)

    request = request_factory(method='get')
    endpoint = MessageInfoEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request, message_id=message_id)


@pytest.mark.asyncio
async def test_info_message_get_if_sender_deleted(patched_context, valid_request_body, request_factory,
                                                  mocker,
                                                  config_test, deleted_valid_user):
    user_id = 1
    message_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.messages.info.get_user', return_value=deleted_valid_user)

    request = request_factory(method='get')
    endpoint = MessageInfoEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request, message_id=message_id)


@pytest.mark.asyncio
async def test_info_message_get_if_message_not_exists(patched_context, valid_request_body, request_factory,
                                                      mocker,
                                                      config_test, valid_user):
    user_id = 1
    message_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.messages.info.get_user', return_value=valid_user)
    mocker.patch('transport.sanic.endpoints.messages.info.get_message', return_value=None)

    request = request_factory(method='get')
    endpoint = MessageInfoEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicMessageNotFoundException):
        await endpoint(request, message_id=message_id)


@pytest.mark.asyncio
async def test_info_message_get_if_message_deleted(patched_context, valid_request_body, request_factory,
                                                   mocker,
                                                   config_test, valid_user, deleted_valid_message):
    user_id = 1
    message_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.messages.info.get_user', return_value=valid_user)
    mocker.patch('transport.sanic.endpoints.messages.info.get_message', return_value=deleted_valid_message)

    request = request_factory(method='get')
    endpoint = MessageInfoEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicMessageNotFoundException):
        await endpoint(request, message_id=message_id)


@pytest.mark.asyncio
async def test_info_message_get_correct_work(patched_context, valid_request_body, request_factory,
                                             mocker,
                                             config_test, valid_user, valid_message):
    user_id = 1
    message_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.messages.info.get_user', return_value=valid_user)
    mocker.patch('transport.sanic.endpoints.messages.info.get_message', return_value=valid_message)

    request = request_factory(method='get')
    endpoint = MessageInfoEndpoint(config_test, patched_context, '', (), True)
    response = await endpoint(request, message_id=message_id)
    assert response.status == 200
