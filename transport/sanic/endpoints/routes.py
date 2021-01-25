from typing import Tuple

from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context) -> Tuple:
    return(
        endpoints.HealthEndpoint(config=config, uri='/', methods=('POST', 'GET'), context=context),
        endpoints.CreateEmployeeEndpoint(config=config, uri='/employee', methods=('POST',), context=context),
        endpoints.CreateUserEndpoint(config=config, uri='/user', methods=('POST',), context=context)
    )