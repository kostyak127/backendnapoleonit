from db.config import SQLiteConfig
from helpers.token.config import TokenConfig
from transport.sanic.config import SanicConfig


class ApplicationConfig:
    sanic: SanicConfig
    token: TokenConfig
    database: SQLiteConfig

    def __init__(self):
        self.sanic = SanicConfig()
        self.database = SQLiteConfig()
        self.token = TokenConfig()