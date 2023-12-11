from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import datetime

DATABASE_URL = "sqlite:///books.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(), nullable=False)
    author = Column(String(), nullable=False)
    genre = Column(String(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class BookPydantic(BaseModel):
    title: str
    author: str
    genre: str

Base.metadata.create_all(bind=engine)

def create_book(db_item: BookPydantic):
    db_item = Book(**db_item.dict())
    with SessionLocal() as db:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item

def retrieve_item(book_id: int):
    with SessionLocal() as db:
        db_item = db.query(Book).filter(Book.id == book_id).first()
        return db_item

def update_item(book_id: int, updated_data: BookPydantic):
    with SessionLocal() as db:
        db_item = db.query(Book).filter(Book.id == book_id).first()
        if db_item:
            for field, value in updated_data.dict().items():
                setattr(db_item, field, value)
            db.commit()
            db.refresh(db_item)
        return db_item

def delete_item(book_id: int):
    with SessionLocal() as db:
        db_item = db.query(Book).filter(Book.id == book_id).first()
        if db_item:
            db.delete(db_item)
            db.commit()
        return db_item