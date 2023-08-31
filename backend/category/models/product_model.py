from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from shared.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(30))
    quantity = Column(Integer)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
    owner_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
