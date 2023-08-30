from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from shared.database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(30), unique=True)
