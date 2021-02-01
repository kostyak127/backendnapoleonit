from sqlalchemy import Column, VARCHAR, VARBINARY, BOOLEAN

from db.models import BaseModel


class DBUser(BaseModel):
    __tablename__ = 'users'

    login = Column(VARCHAR(50), unique=True, nullable=False)

    password = Column(VARBINARY(), unique=True, nullable=False)

    first_name = Column(VARCHAR(50))

    last_name = Column(VARCHAR(50))

    is_delete = Column(BOOLEAN, nullable=False, default=False)