from sqlalchemy.orm import Session

import models
import schemas

#AUTHORS
def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_email(db: Session, email: str):
    return db.query(models.Author).filter(models.Author.email == email).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    fake_hashed_password = author.password + "notreallyhashed"
    db_author = models.Author(email=author.email, hashed_password=fake_hashed_password, \
                              first_name=author.first_name, last_name=author.last_name, \
                              place_of_birth=author.place_of_birth, biography=author.biography)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

#BOOKS
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_author_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if book:
        db.delete(book)
        db.commit()
        return book
    return None

#PEN NAMES
def create_author_pen_name(db:Session, pen_name: schemas.PenNameCreate, author_id: int):
    db_pen_name = models.PenName(**pen_name.dict(),author_id=author_id)
    db.add(db_pen_name)
    db.commit()
    db.refresh(db_pen_name)
    return db_pen_name

def get_pen_name(db: Session, pen_name_id: int):
    return db.query(models.PenName).filter(models.PenName.id == pen_name_id).first()


def delete_pen_name(db: Session, pen_name_id: int):
    pen_name = get_pen_name(db, pen_name_id)
    if pen_name:
        db.delete(pen_name)
        db.commit()
        return pen_name
    return None
