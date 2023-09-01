from shared.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    seller_id = Column(Integer, ForeignKey("products.owner_id"))
    customer_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer)
    timestamp = Column(DateTime)

