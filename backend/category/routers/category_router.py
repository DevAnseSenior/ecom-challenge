from typing import List, Type

from fastapi import APIRouter, Depends
from pydantic import BaseModel
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
    description: str


@router.get("", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryResponse]:
    return db.query(Category).all()


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
