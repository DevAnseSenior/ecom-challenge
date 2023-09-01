from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String

from shared.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
