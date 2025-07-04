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
router = APIRouter(
    tags=["books"],
    prefix="/books",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class BookRequest(BaseModel):
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


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page")
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


# Book pages
@router.get("/book-page")
async def book_page(request: Request, db: db_dependency):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return redirect_to_login()
    try:
        user = await get_current_user(access_token)
        if user is None:
            return redirect_to_login()
        books = db.query(Book).filter(Book.owner_id == user["id"]).all()
        return templates.TemplateResponse(
            "book.html", {"request": request, "books": books, "user": user}
        )
    except Exception:
        return redirect_to_login()


@router.get("/add-book-page")
async def add_book_page(request: Request, db: db_dependency):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return redirect_to_login()
    try:
        user = await get_current_user(access_token)
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse(
            "add-book.html", {"request": request, "user": user}
        )
    except Exception:
        return redirect_to_login()


@router.get("/edit-book-page/{id}")
async def edit_book_page(request: Request, db: db_dependency, id: int = Path(gt=0)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return redirect_to_login()
    try:
        user = await get_current_user(access_token)
        if user is None:
            return redirect_to_login()
        book = db.query(Book).filter(Book.id == id, Book.owner_id == user["id"]).first()
        if book is None:
            return redirect_to_login()
        return templates.TemplateResponse(
            "edit-book.html", {"request": request, "user": user, "book": book}
        )
    except Exception:
        return redirect_to_login()


# Book endpoints
@router.get("/books/", status_code=status.HTTP_200_OK)
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


@router.get("/books/{pk}", status_code=status.HTTP_200_OK)
async def get_book_by_id(
    db: db_dependency, user: user_dependency, pk: int = Path(gt=0)
):
    query = db.query(Book).filter(getattr(Book, "id") == pk)
    book = query.first()
    if book:
        return book
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/book/", status_code=status.HTTP_201_CREATED)
async def create_book(
    book_request: BookRequest, db: db_dependency, user: user_dependency
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    new_book = Book(**book_request.model_dump(), owner_id=user["id"])
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.put("/book/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(
    db: db_dependency, user: user_dependency, book: BookRequest, id: int = Path(gt=0)
):
    query = db.query(Book).filter(Book.id == id, Book.owner_id == user["id"]).first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        setattr(query, "title", book.title)
        setattr(query, "description", book.description)
        setattr(query, "author", book.author)
        setattr(query, "published_date", book.published_date)
        setattr(query, "rating", book.rating)
        setattr(query, "owner_id", user["id"])
    db.add(query)
    db.commit()
    return status.HTTP_200_OK


@router.delete("/book/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(user: user_dependency, db: db_dependency, pk: int = Path(gt=0)):
    query = db.query(Book).filter(Book.id == pk, Book.owner_id == user["id"]).first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        db.query(Book).filter(Book.id == pk).delete()
        db.commit()

    return status.HTTP_204_NO_CONTENT
