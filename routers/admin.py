from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from models import Book
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

router = APIRouter(
    tags=["admin"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/admin/books/", status_code=status.HTTP_200_OK)
async def get_all_books(user: user_dependency, db: db_dependency):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return db.query(Book).all()


@router.get("/admin/books/{id}", status_code=status.HTTP_200_OK)
async def get_book(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    queryset = db.query(Book).filter(Book.id == id).first()  # type: ignore
    if queryset is not None:
        return queryset
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/admin/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db: db_dependency, id: int = Path(gt=0)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    queryset = db.query(Book).filter(Book.id == id).first()  # type: ignore
    if queryset is not None:
        db.delete(queryset)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
