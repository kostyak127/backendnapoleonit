from sqlalchemy import VARCHAR, Column, INT

from db.models import BaseModel


class DBEmployee(BaseModel):
    __tablename__ = 'employees'
    firstname = Column(VARCHAR(50))
    lastname = Column(VARCHAR(50))
    user_id = Column(INT())