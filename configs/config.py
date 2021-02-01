from db.config import PostgreSQLConfig
from helpers.token.config import TokenConfig
from transport.sanic.config import SanicConfig


class ApplicationConfig:
    sanic: SanicConfig
    database: PostgreSQLConfig
    token: TokenConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.database = PostgreSQLConfig()
        self.token = TokenConfig()