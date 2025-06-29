from typing import Optional
from fastapi import Body, Path, Query, HTTPException, status, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


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


Books = [
    Book(1, "The Forty Rules of Love", "Elif Shafak", "Literary Fiction", 6, 2012),
    Book(2, "A Court of Thorns and Roses", "Sarah J. Maas", "Romance", 5, 2009),
    Book(3, "The Hobbit", "J. Tolkien", "Fantasy", 7, 1999),
    Book(4, "Pride and Prejudice", "Jane Austen", "Fiction", 6, 2024),
]


@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_query_params(
    description: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    rating: Optional[int] = Query(None, ge=0, le=10),
):
    querried_books = []
    for book in Books:
        if (
            (rating is None or book.rating == rating)
            and (
                author is None or book.author.lower() == author.lower()
                if author
                else True
            )
            and (
                description is None or book.description.lower() == description.lower()
                if description
                else True
            )
        ):
            querried_books.append(book)
    return querried_books


@app.get("/books/{pk}", status_code=status.HTTP_200_OK)
async def get_book_by_id(pk: int = Path(gt=0)):
    for book in Books:
        if book.id == pk:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/books/create", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(Books) > 0:
        book.id = Books[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_updated = False
    for i in range(len(Books)):
        if Books[i].id == book.id:
            Books[i] = Book(**book.model_dump())
            book_updated = True
    if not book_updated:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(pk: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(Books)):
        if Books[i].id == pk:
            Books.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
