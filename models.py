from database import Base
from sqlalchemy import Column, Date, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String)
    rating = Column(Integer)
    published_date = Column(Date)
    author_id = Column(Integer, ForeignKey("users.id"))

    def __init__(
        self, id, title, author, description, rating, published_date, author_id
    ) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        self.author_id = author_id
