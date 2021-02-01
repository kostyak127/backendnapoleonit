from api.request.user.create import RequestCreateUserDto
from api.request.user.modify_info import RequestModifyUserInfoDto
from db.database import DBSession
from db.exceptions import DBUserExistsException, DBUserNotExistsException
from db.models import DBUser


def create_user(session: DBSession, user: RequestCreateUserDto, hashed_password: bytes) -> DBUser:
    new_user = DBUser(
        login=user.login,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        is_delete=user.is_delete
    )
    if session.get_user_by_login(user.login) is not None:
        raise DBUserExistsException
    session.add_model(new_user)
    return new_user


def get_user(session: DBSession, *, login: str = None, user_id: int = None) -> DBUser:
    if login is not None:
        user = session.get_user_by_login(login)
    else:
        user = session.get_user_by_id(user_id)

    if user is None or user.is_delete:
        raise DBUserNotExistsException

    return user


def modify_user(session: DBSession, *, to_modify: RequestModifyUserInfoDto, user_id: int):
    db_user = session.get_user_by_id(user_id)
    if db_user is None or db_user.is_delete:
        raise DBUserNotExistsException

    for attr in to_modify.fields:
        value = getattr(to_modify, attr)
        setattr(db_user, attr, value)

    return db_user


def delete_user(session: DBSession, user_id: int):
    db_user = session.get_user_by_id(user_id)
    if db_user is None or db_user.is_delete:
        raise DBUserNotExistsException

    db_user.is_delete = True

    return db_user