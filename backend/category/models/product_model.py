from sqlalchemy import Column, Integer, String

from shared.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(30))
    quantity = Column(Integer)
