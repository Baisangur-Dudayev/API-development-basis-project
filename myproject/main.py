from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String, index=True)
    place_of_birth = Column(String)
    biography = Column(String)
    is_active = Column(Boolean, default=True)

    # relatie met classe PenName
    pen_names = relationship("PenName", back_populates="author2")

    # relatie met classe Book
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    publication_date = Column(String)
    genre = Column(String)
    #FK
    author_id = Column(Integer, ForeignKey("authors.id"))

    # relatie met classe Author
    author = relationship("Author", back_populates="books")


class PenName(Base):
    __tablename__ = "pen_names"

    id = Column(Integer, primary_key=True, index=True)
    pen_name = Column(String, index=True)
    #FK
    author_id = Column(Integer, ForeignKey("authors.id"))

    # relatie met classe Author
    author2 = relationship("Author", back_populates="pen_names")
