from typing import List

from app.routers.product_router import ProductResponse, Product
from fastapi import APIRouter, Depends
from shared.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")


@router.get("/{id_user}/products", response_model=List[ProductResponse])
def get_products_from_user(id_user: int,
                           db: Session = Depends(get_db)) -> List[ProductResponse]:
    return db.query(Product).filter_by(owner_id=id_user).all()
