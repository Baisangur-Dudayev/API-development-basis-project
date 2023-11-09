from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
import os

if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#AUTHORS
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_email(db, email=author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

#BOOKS
@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(
    author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)
):
    return crud.create_author_book(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book_for_author(book_id: int, db: Session = Depends(get_db)):
    book = crud.delete_book(db=db, book_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

#PENNAMES
@app.post("/authors/{author_id}/pen_names/",response_model=schemas.PenName)
def create_pen_name_for_author(
    author_id: int, pen_name: schemas.PenNameCreate, db:Session = Depends(get_db)
):
    return crud.create_author_pen_name(db=db, pen_name=pen_name, author_id=author_id)

@app.delete("/pen_names/{pen_name_id}", response_model=schemas.PenName)
def delete_pen_name(pen_name_id: int, db: Session = Depends(get_db)):
    pen_name = crud.delete_pen_name(db=db, pen_name_id=pen_name_id)
    if pen_name:
        return pen_name
    raise HTTPException(status_code=404, detail="Pen Name not found")

