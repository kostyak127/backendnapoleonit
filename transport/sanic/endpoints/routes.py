from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return(
        endpoints.HealthEndpoint(
            config=config, uri='/', methods=['POST', 'GET'], context=context),
        endpoints.CreateUserEndpoint(
            config=config, uri='/user', methods=['POST'], context=context),
        endpoints.AuthUserEndpoint(
            config=config, uri='/auth', methods=['POST'], context=context),
        endpoints.InfoUserEndpoint(
            config=config, uri='/user/<user_id:int>', methods=['GET', 'PATCH'], context=context, need_auth=True),
        endpoints.DeleteUserEndpoint(
            config=config, uri='/delete_user/<user_id:int>', methods=['DELETE'], context=context, need_auth=True),
        endpoints.MessageEndpoint(
            config=config, uri='/message', methods=['GET', 'POST'], context=context, need_auth=True),
        endpoints.MessageInfoEndpoint(
            config=config, uri='/message/<message_id:int>', methods=['GET', 'PATCH', 'DELETE'],
            context=context, need_auth=True),
    )