from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from shared.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
