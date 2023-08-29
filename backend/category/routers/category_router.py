from typing import List, Type

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from category.models.category_model import Category
from shared.dependencies import get_db

router = APIRouter(prefix="/categories")


class CategoryResponse(BaseModel):
    id: int
    description: str

    class Config:
        orm_mode: True


class CategoryRequest(BaseModel):
    description: str = Field(min_length=3, max_length=30)


@router.get("", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)) -> list[Type[Category]]:
    return db.query(Category).all()


@router.get("/{id_category}", response_model=CategoryResponse)
def get_category(id_category: int,
                 db: Session = Depends(get_db)) -> list[Type[Category]]:
    category: Category = db.query(Category).get(id_category)
    return category


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(category_request: CategoryRequest,
                    db: Session = Depends(get_db)) -> CategoryResponse:
    category = Category(
        **category_request.model_dump()
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.put("/{id_category}", response_model=CategoryResponse, status_code=200)
def update_category(id_category: int,
                    category_request: CategoryRequest,
                    db: Session = Depends(get_db)) -> CategoryResponse:
    category = db.query(Category).get(id_category)
    category.description = category_request.description

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{id_category}", status_code=204)
def delete_category(id_category: int,
                    db: Session = Depends(get_db)) -> None:
    category = db.query(Category).get(id_category)
    db.delete(category)
    db.commit()
