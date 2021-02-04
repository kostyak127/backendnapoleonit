from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session

from db.exceptions import DBIntegrityException, DBDataException
from db.models import BaseModel, DBUser, DBMessage


class DBSession:
    _session: Session

    def __init__(self, session):
        self._session = session

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)

    def close_session(self):
        self._session.close()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as error:
            raise DBIntegrityException(error)
        except DataError as error:
            raise DBDataException(error)

    def commit_session(self, need_close: bool = False):
        try:
            self._session.commit()
        except IntegrityError as error:
            raise DBIntegrityException(error)
        except DataError as error:
            raise DBDataException(error)

        if need_close:
            self._session.close()

    def get_user_by_login(self, login: str) -> DBUser:
        return self._session.query(DBUser).filter(DBUser.login == login).first()

    def get_user_by_id(self, user_id: int) -> DBUser:
        return self._session.query(DBUser).filter(DBUser.id == user_id).first()

    def get_user_messages(self, user_id: int) -> List[DBMessage]:
        return self._session.query(DBMessage).filter((DBMessage.is_delete == 0)
                    and (DBMessage.sender_id == user_id or DBMessage.recipient_id == user_id)).all()

    def get_message_by_id(self, message_id: int) -> DBMessage:
        return self._session.query(DBMessage).filter(DBMessage.id == message_id).first()


class Database:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)