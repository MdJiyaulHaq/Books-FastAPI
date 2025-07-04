from typing import Optional
from fastapi import APIRouter, Body, Path, Query, HTTPException, status, FastAPI
from pydantic import BaseModel, Field
from models import Book
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.params import Body
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

app = FastAPI()

router = APIRouter(
    tags=["books"],
)


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="Id is not required while creating a book.", default=None
    )
    title: str = Field(max_length=100, min_length=3)
    author: str = Field(max_length=100, min_length=3)
    description: str = Field(max_length=255, min_length=5)
    rating: int = Field(ge=0, le=10)
    published_date: int = Field(ge=1999, le=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Name of a book",
                "author": "Md",
                "description": "A detailed description of the book.",
                "rating": 9,
                "published_date": 2020,
            }
        }
    }


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_query_params(
    user: user_dependency,
    db: db_dependency,
    description: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    rating: Optional[int] = Query(None, ge=0, le=10),
):
    query = db.query(Book)
    if rating is not None:
        query = query.filter(getattr(Book, "rating") == rating)
    if author is not None:
        query = query.filter(getattr(Book, "author") == author)
    if description is not None:
        query = query.filter(getattr(Book, "description") == description)
    books = query.all()
    return books


@app.get("/books/{pk}", status_code=status.HTTP_200_OK)
async def get_book_by_id(
    db: db_dependency, user: user_dependency, pk: int = Path(gt=0)
):
    query = db.query(Book).filter(getattr(Book, "id") == pk)
    book = query.first()
    if book:
        return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/books/create", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_request: BookRequest, db: db_dependency, user: user_dependency
):
    new_book = Book(**book_request.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put("/books/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest, db: db_dependency, user: user_dependency):
    query = db.query(Book).filter(getattr(Book, "id") == book.id)
    book_to_update = query.first()
    if book_to_update:
        for key, value in book.model_dump().items():
            setattr(book_to_update, key, value)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db: db_dependency, pk: int = Path(gt=0)):
    query = db.query(Book).filter(getattr(Book, "id") == pk)
    book_to_delete = query.first()
    if book_to_delete:
        db.delete(book_to_delete)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Item not found")
