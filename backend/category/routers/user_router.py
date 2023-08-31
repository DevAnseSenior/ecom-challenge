from typing import List

from category.models.user_model import User, password_context
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from shared.dependencies import get_db
from shared.exceptions import NotFound
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")


class UserResponse(BaseModel):
    id: int
    username: str
    hashed_password: str
    email: str

    class Config:
        orm_mode: True


class UserLogin(BaseModel):
    username: str
    hashed_password: str


class UserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    hashed_password: str
    email: str


@router.get("", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)) -> List[User]:
    return db.query(User).all()


@router.get("/{id_user}", response_model=UserResponse)
def get_user(id_user: int,
             db: Session = Depends(get_db)) -> List[User]:
    return find_user_by_id(id_user, db)


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_request: UserRequest,
                  db: Session = Depends(get_db)) -> UserResponse:
    hashed_password = password_context.hash(user_request.hashed_password)
    user = User(
        username=user_request.username,
        hashed_password=hashed_password,
        email=user_request.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/{id_user}", response_model=UserResponse, status_code=200)
def update_user(id_user: int,
                user_request: UserRequest,
                db: Session = Depends(get_db)) -> UserResponse:
    user = find_user_by_id(id_user, db)
    user.username = user_request.username
    user.hashed_password = user_request.hashed_password
    user.email = user_request.email

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{id_user}", status_code=204)
def delete_user(id_user: int,
                db: Session = Depends(get_db)) -> None:
    user = find_user_by_id(id_user, db)
    db.delete(user)
    db.commit()


def find_user_by_id(id_user: int, db: Session) -> User:
    user = db.query(User).get(id_user)
    if user is None:
        raise NotFound("User")

    return user


@router.post("/login/")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user or not password_context.verify(user_login.hashed_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Logged in sucessfull"}
