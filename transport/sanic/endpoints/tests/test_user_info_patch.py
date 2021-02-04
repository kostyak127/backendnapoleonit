import pytest

from transport.sanic.endpoints import InfoUserEndpoint


@pytest.mark.asyncio
async def test_info_user_patch_correct_work(patched_context, valid_request_body, request_factory, mocker,
                                          config_test, valid_user):
    user_id = 1
    mocker.patch('transport.sanic.base.SanicEndpoint.get_request_body', return_value=valid_request_body)
    mocker.patch('transport.sanic.base.SanicEndpoint.import_body_auth', return_value={'user_id': user_id})
    mocker.patch('transport.sanic.endpoints.users.info.get_user', return_value=valid_user)
    mocker.patch('transport.sanic.endpoints.users.info.modify_user', return_value=valid_user)

    request = request_factory(method='get')
    endpoint = InfoUserEndpoint(config_test, patched_context, '', (), True)
    response = await endpoint(request, user_id=user_id)

    assert response.status == 200