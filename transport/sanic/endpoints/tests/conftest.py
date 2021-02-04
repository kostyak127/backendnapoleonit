import pytest
import sqlalchemy

from context import Context
from db.database import Database, DBSession
from helpers.token.config import TokenConfig


@pytest.fixture()
def request_factory():
    class Request:
        def __init__(
                self,
                method: str = 'get',
                user_id: int = 1,
                content_type: str = '',
                headers: dict = None,
                json: str = None,
        ):
            self.method = method.upper()
            self.user_id = user_id
            self.content_type = content_type
            self.headers = headers or {}
            self.json = json

    return Request


@pytest.fixture()
def patched_context(patched_db) -> Context:
    context = Context()
    context.set('database', patched_db)

    return context


@pytest.fixture()
def patched_db(mocker):
    patched_engine = mocker.patch.object(sqlalchemy, 'create_engine')
    patched_engine.return_value = None

    patched_make_session = mocker.patch.object(Database, 'make_session')
    patched_make_session.return_value = DBSession(session=None)

    return Database


@pytest.fixture()
def valid_request_body():
    return {"login": "ko", "password": "q", "first_name": "kostya", "last_name": "korotchenkov",
            "message": "message", "recipient": "login"}


@pytest.fixture()
def config_test():
    class Config:
        token = TokenConfig()

    return Config()


@pytest.fixture()
def valid_user():
    class User:
        is_delete = False
        password = 'q'
        login = 'ko'
        first_name = 'kostya'
        last_name = 'korotchenkov'
        created_at = '2021-02-02 03:29:15.564675'
        updated_at = '2021-02-02 03:29:15.564675'
        id = 1

    return User()


@pytest.fixture()
def deleted_valid_user():
    class User:
        is_delete = True
        password = 'q'
        login = 'ko'
        first_name = 'kostya'
        last_name = 'korotchenkov'
        created_at = '2021-02-02 03:29:15.564675'
        updated_at = '2021-02-02 03:29:15.564675'
        id = 1

    return User()


@pytest.fixture()
def session():
    class Session:
        def commit_session(self):
            pass

    return Session


@pytest.fixture()
def valid_message():
    class Message:
        id = 1
        created_at = '2021-02-02 03:29:15.564675'
        updated_at = '2021-02-02 03:29:15.564675'
        sender_id = 1
        recipient_id = 2
        message = 'message'
        is_delete = False

    return Message()


@pytest.fixture()
def deleted_valid_message():
    class Message:
        id = 1
        created_at = '2021-02-02 03:29:15.564675'
        updated_at = '2021-02-02 03:29:15.564675'
        sender_id = 1
        recipient_id = 2
        message = 'message'
        is_delete = True

    return Message()
