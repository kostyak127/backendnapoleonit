from sqlalchemy import Column, VARCHAR

from db.models import BaseModel


class DBUser(BaseModel):
    __tablename__ = 'users'

    login = Column(
        VARCHAR(50),
        unique=True,
        nullable=False
    )

    password = Column(
        VARCHAR(50),
        unique=True,
        nullable=False
    )