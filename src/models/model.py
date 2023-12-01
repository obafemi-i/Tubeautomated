from sqlalchemy import Integer, String, Column
from .database import Base

class User(Base):
    __tablename__ = 'editors'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(20), unique=True, index=True)
    password = Column(String(170))
    first_name = Column(String(20), index=True)

