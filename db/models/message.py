from sqlalchemy import Column, Integer, VARCHAR, BOOLEAN

from db.models import BaseModel


class DBMessage(BaseModel):
    __tablename__ = 'messages'

    sender_id = Column(Integer, nullable=False)

    recipient_id = Column(Integer, nullable=False)

    message = Column(VARCHAR(1000), nullable=False)

    is_delete = Column(BOOLEAN, nullable=False, default=False)