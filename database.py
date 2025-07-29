from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://books_database_v0ap_user:6nvk5m7SfaJYIRqrnWKORoq1lbpE4mpw@dpg-d20q0iemcj7s73e1dj80-a/books_database_v0ap"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()
