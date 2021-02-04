from typing import List

from api.request.message.create import RequestCreateMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistsException, DBMessageNotExistsException
from db.models import DBMessage
from db.queries.user import get_user


def create_message(session: DBSession, message: RequestCreateMessageDto, sender_id: int) -> DBMessage:
    recipient = get_user(session, login=message.recipient)

    new_message = DBMessage(
        message=message.message,
        recipient_id=recipient.id,
        sender_id=sender_id
    )

    session.add_model(new_message)

    return new_message


def get_user_messages(session: DBSession, user_id: int) -> List[DBMessage]:
    messages = session.get_user_messages(user_id)
    return messages if messages else []


def get_message(session: DBSession, message_id: int) -> DBMessage:
    message = session.get_message_by_id(message_id)

    return message


def modify_message(session: DBSession, message_id: int, message_text: str) -> DBMessage:
    message = session.get_message_by_id(message_id)

    message.message = message_text

    return message


def delete_message(session: DBSession, message_id: int) -> DBMessage:
    message = session.get_message_by_id(message_id)

    message.is_delete = True

    return message


def check_message_exists(message: DBMessage):
    if message is None or message.is_delete:
        raise DBMessageNotExistsException
