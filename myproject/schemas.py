from pydantic import BaseModel

#Book classen
class BookBase(BaseModel):
    title: str
    description: str | None = None
    publication_date: str
    genre: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

#PenName classen
class PenNameBase(BaseModel):
    pen_name: str

class PenNameCreate(PenNameBase):
    pass

class PenName(PenNameBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

#Author classen
class AuthorBase(BaseModel):
    email: str
    first_name: str | None = None
    last_name: str  | None = None
    place_of_birth: str | None = None
    biography: str | None = None

class AuthorCreate(AuthorBase):
    password: str

class Author(AuthorBase):
    id: int
    is_active: bool
    #om classen Book & PenName hier te gebruiken moeten ze boven boven deze classen gedefinieerd staan
    books: list[Book] = []
    pen_names: list[PenName] = []

    class Config:
        orm_mode = True

