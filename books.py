from fastapi import Body, FastAPI

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


@app.delete("/books/{pk}/delete")
async def delete_book(pk: int):
    if Books[pk].get("id"):
        Books.pop(pk)
    return {"book deleted successfully"}
