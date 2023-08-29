from sqlalchemy import Column, Integer, String

from shared.database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(30))
