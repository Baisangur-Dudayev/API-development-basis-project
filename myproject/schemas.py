from pydantic import BaseModel, Field
#^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$    from 
#Book classen
class BookBase(BaseModel):
    title: str
    description: str | None = None
    publication_date: str 
   # publication_date: str = Field(
    #    ...,  # Ensure the field is required
     #   description="Publication date in the format YYYY-MM-DD",
      #  regex=r"^\d{4}-\d{2}-\d{2}$",
   # )
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

#Author classen ^[a-zA-Z]+$
class AuthorBase(BaseModel):
    email: str = Field(pattern='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$') 
    first_name: str | None = Field(pattern='^[a-zA-Z]+$')
    last_name: str  | None = Field(pattern='^[a-zA-Z]+$')
    place_of_birth: str | None = Field(pattern='^[a-zA-Z]+$')
    biography: str | None = None

class AuthorCreate(AuthorBase):
     password: str = Field(
        ...,  # This indicates that the password is required
        min_length=8,  # Enforces a minimum length of 8 characters
    )

class Author(AuthorBase):
    id: int
    is_active: bool
    #om classen Book & PenName hier te gebruiken moeten ze boven boven deze classen gedefinieerd staan
    books: list[Book] = []
    pen_names: list[PenName] = []

    class Config:
        orm_mode = True

