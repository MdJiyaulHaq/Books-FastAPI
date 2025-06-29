from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="Id is not required while creating a book.", default=None
    )
    title: str = Field(max_length=100, min_length=3)
    author: str = Field(max_length=100, min_length=3)
    description: str = Field(max_length=255, min_length=5)
    rating: int = Field(ge=0, le=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Name of a book",
                "author": "Md",
                "description": "A detailed description of the book.",
                "rating": 9,
            }
        }
    }


Books = [
    Book(1, "The Forty Rules of Love", "Elif Shafak", "Literary Fiction", 6),
    Book(2, "A Court of Thorns and Roses", "Sarah J. Maas", "Romance", 5),
    Book(3, "The Hobbit", "J. Tolkien", "Fantasy", 7),
    Book(4, "Pride and Prejudice", "Jane Austen", "Fiction", 6),
]


@app.get("/books")
async def get_books():
    return Books


@app.get("/books/{pk}")
async def get_book_by_id(pk: int):
    for book in Books:
        if book.id == pk:
            return book
    return {"error": "Book not found"}


@app.get("/books/")
async def get_book_by_query_params(category: str, author: str):
    querried_books = []
    for book in Books:
        category_value = book.get("category")
        author_value = book.get("author")
        if (
            category_value is not None
            and author_value is not None
            and category_value.casefold() == category.casefold()
            and author_value.casefold() == author.casefold()
        ):
            querried_books.append(book)
    return querried_books


@app.post("/books/create")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    Books.append(find_book_id(new_book))
    return {"book added successfully"}


def find_book_id(book: Book):
    if len(Books) > 0:
        book.id = Books[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update")
async def update_book(updated_book=Body()):
    for i in range(len(Books)):
        if Books[i].get("id") == updated_book.get("id"):
            Books[i] = updated_book
    return {"book updated successfully"}


@app.delete("/books/{pk}/delete")
async def delete_book(pk: int):
    if Books[pk].get("id"):
        Books.pop(pk)
    return {"book deleted successfully"}
