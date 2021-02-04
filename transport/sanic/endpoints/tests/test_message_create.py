import pytest

from transport.sanic.endpoints import MessageEndpoint
from transport.sanic.exceptions import SanicUserNotFoundException


@pytest.mark.asyncio
async def test_create_message_if_sender_or_recipient_not_exists(patched_context, valid_request_body, request_factory,
                                                                mocker,
                                                                config_test):
    user_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    # mocker.patch('db.database.Database.make_session', return_value=session())
    mocker.patch('transport.sanic.endpoints.messages.create_get_list.get_user', return_value=None)

    request = request_factory(method='post')
    endpoint = MessageEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request, user_id=user_id)


@pytest.mark.asyncio
async def test_create_message_if_sender_or_recipient_is_delete(patched_context, valid_request_body, request_factory,
                                                               mocker,
                                                               config_test, deleted_valid_user):
    user_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    # mocker.patch('db.database.Database.make_session', return_value=session())
    mocker.patch('transport.sanic.endpoints.messages.create_get_list.get_user', return_value=deleted_valid_user)

    request = request_factory(method='post')
    endpoint = MessageEndpoint(config_test, patched_context, '', (), True)

    with pytest.raises(SanicUserNotFoundException):
        await endpoint(request, user_id=user_id)


@pytest.mark.asyncio
async def test_create_message_correct_work(patched_context, valid_request_body, request_factory,
                                           mocker,
                                           config_test, session, valid_user, valid_message):
    user_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('db.database.Database.make_session', return_value=session())
    mocker.patch('transport.sanic.endpoints.messages.create_get_list.get_user', return_value=valid_user)
    mocker.patch('transport.sanic.endpoints.messages.create_get_list.create_message', return_value=valid_message)

    request = request_factory(method='post')
    endpoint = MessageEndpoint(config_test, patched_context, '', (), True)
    response = await endpoint(request)

    assert response.status == 201