from typing import List, Type

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from category.models.product_model import Product
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/products")


class ProductResponse(BaseModel):
    id: int
    description: str
    quantity: int

    class Config:
        orm_mode: True


class ProductRequest(BaseModel):
    description: str = Field(min_length=3, max_length=255)
    quantity: int


@router.get("", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)) -> list[Type[Product]]:
    return db.query(Product).all()


@router.get("/{id_product}", response_model=ProductResponse)
def get_product(id_product: int,
                db: Session = Depends(get_db)) -> list[Type[Product]]:
    return find_product_by_id(id_product, db)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(product_request: ProductRequest,
                   db: Session = Depends(get_db)) -> ProductResponse:
    product = Product(
        **product_request.model_dump()
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@router.put("/{id_product}", response_model=ProductResponse, status_code=200)
def update_product(id_product: int,
                   product_request: ProductRequest,
                   db: Session = Depends(get_db)) -> ProductResponse:
    product = find_product_by_id(id_product, db)
    product.description = product_request.description
    product.quantity = product_request.quantity

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{id_product}", status_code=204)
def delete_product(id_product: int,
                   db: Session = Depends(get_db)) -> None:
    product = find_product_by_id(id_product, db)
    db.delete(product)
    db.commit()


def find_product_by_id(id_product: int, db: Session) -> Product:
    product = db.query(Product).get(id_product)
    if product is None:
        raise NotFound("Product")

    return product
