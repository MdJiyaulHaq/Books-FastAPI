from fastapi import Body, FastAPI

app = FastAPI()

Books = [
    {
        "id": 1,
        "title": "The Forty Rules of Love",
        "author": "Elif Shafak",
        "category": "Literary Fiction",
    },
    {
        "id": 2,
        "title": "A Court of Thorns and Roses",
        "author": "Sarah J. Maas",
        "category": "Romance",
    },
    {
        "id": 3,
        "title": "The Hobbit",
        "author": "J. Tolkien",
        "category": "Fantasy",
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "category": "Fiction",
    },
]


@app.get("/books")
async def get_books():
    return Books


@app.get("/books/{pk}")
async def get_book_by_id(pk: int):
    for book in Books:
        if book.get("id") == pk:
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
async def create_book(new_book=Body()):
    Books.append(new_book)
    return {"book added successfully"}


@app.put("/books/update")
async def update_book(updated_book=Body()):
    for i in range(len(Books)):
        if Books[i].get("id") == updated_book.get("id"):
            Books[i] = updated_book
    return {"book updated successfully"}
