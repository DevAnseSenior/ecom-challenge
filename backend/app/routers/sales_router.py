from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.sales_model import Sale
from app.routers.product_router import update_quantity, find_product_by_id
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/sales")


class SaleResponse(BaseModel):
    id: int
    product_id: int
    seller_id: int
    customer_id: int
    quantity: int
    timestamp: datetime

    class Config:
        orm_mode: True


class SaleRequest(BaseModel):
    product_id: int
    seller_id: int
    customer_id: int
    quantity: int
    timestamp: datetime


@router.get("", response_model=List[SaleResponse])
def list_sales(db: Session = Depends(get_db)) -> List[Sale]:
    return db.query(Sale).all()


@router.get("/{id_sale}", response_model=SaleResponse)
def get_sale(id_sale: int,
             db: Session = Depends(get_db)) -> List[Sale]:
    return find_sale_by_id(id_sale, db)


@router.post("/register", response_model=SaleResponse, status_code=201)
def register_sale(sale_request: SaleRequest,
                  db: Session = Depends(get_db)) -> SaleResponse:

    seller = find_product_by_id(sale_request.product_id, db)
    sale = Sale(
        product_id=sale_request.product_id,
        seller_id=seller.owner_id,
        customer_id=sale_request.customer_id,
        quantity=sale_request.quantity,
        timestamp=datetime.now()
    )

    update_quantity(sale.product_id, sale.quantity, db)

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return sale


def find_sale_by_id(id_sale: int, db: Session) -> Sale:
    sale = db.query(Sale).get(id_sale)
    if sale is None:
        raise NotFound("Sale")

    return sale


