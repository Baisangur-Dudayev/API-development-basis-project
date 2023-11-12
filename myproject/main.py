#code test 21:59
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
#OAuth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import auth

import crud
import models
import schemas
from database import SessionLocal, engine
import os

from fastapi.middleware.cors import CORSMiddleware #voor site & security


if not os.path.exists('.\sqlitedb'):
    os.makedirs('.\sqlitedb')

#"sqlite:///./sqlitedb/sqlitedata.db"
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) Configuration
origins = [
    "*",
    "http://localhost",
    "http://localhost:8095",  # Add your frontend's local development server
    "https://localhost.tiangolo.com",
    "http://127.0.0.1:5500"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific HTTP headers if needed
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#OAuth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Try to authenticate the user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Add the JWT case sub with the subject(user)
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    #Return the JWT as a bearer token to be placed in the headers
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
def read_users_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.get_current_active_user(db, token)
    return current_user

#AUTHORS
@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_email(db, email=author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_author(db=db, author=author)


@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

#BOOKS
@app.post("/authors/{author_id}/books/", response_model=schemas.Book)
def create_book_for_author(author_id: int, book: schemas.BookCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_author_book(db=db, book=book, author_id=author_id)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book_for_author(book_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    book = crud.delete_book(db=db, book_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

#PENNAMES
@app.post("/authors/{author_id}/pen_names/",response_model=schemas.PenName)
def create_pen_name_for_author(author_id: int, pen_name: schemas.PenNameCreate, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.create_author_pen_name(db=db, pen_name=pen_name, author_id=author_id)

@app.delete("/pen_names/{pen_name_id}", response_model=schemas.PenName)
def delete_pen_name(pen_name_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    pen_name = crud.delete_pen_name(db=db, pen_name_id=pen_name_id)
    if pen_name:
        return pen_name
    raise HTTPException(status_code=404, detail="Pen Name not found")

