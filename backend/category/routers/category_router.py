from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/category")


class CategoryResponse(BaseModel):
    id: int
    description: str


class CategoryRequest(BaseModel):
    description: str


@router.get("/", response_model=List[CategoryResponse])
def list_categories():
    return [
        CategoryResponse(
            id=1,
            description="Eletrônico"
        )
    ]


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryRequest):
    return CategoryResponse(
        id=2,
        description=category.description
    )
