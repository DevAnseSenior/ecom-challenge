from typing import List, Type

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from category.models.category_model import Category
from category.models.product_model import Product
from category.models.user_model import User
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/products")


class ProductResponse(BaseModel):
    id: int
    description: str
    price: float
    quantity: int
    category_id: int
    owner_id: int

    class Config:
        orm_mode: True


class ProductRequest(BaseModel):
    description: str = Field(min_length=3, max_length=255)
    price: float
    quantity: int
    category_id: int
    owner_id: int


@router.get("", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)) -> List[Product]:
    return db.query(Product).all()


@router.get("/{id_product}", response_model=ProductResponse)
def get_product(id_product: int,
                db: Session = Depends(get_db)) -> List[Product]:
    return find_product_by_id(id_product, db)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(product_request: ProductRequest,
                   db: Session = Depends(get_db)) -> ProductResponse:

    validate_owner(db, product_request.owner_id)
    validate_category(db, product_request.category_id)

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

    validate_owner(db, product_request.owner_id)
    validate_category(db, product_request.category_id)

    product = find_product_by_id(id_product, db)
    product.description = product_request.description
    product.price = product_request.price
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


def validate_owner(db, owner_id):
    if owner_id is not None:
        user = db.query(User).get(owner_id)
        if user is None:
            raise HTTPException(status_code=422, detail="User don't exists in DB")


def validate_category(db, category_id):
    if category_id is not None:
        category = db.query(Category).get(category_id)
        if category is None:
            raise HTTPException(status_code=422, detail="Category don't exists in DB")
