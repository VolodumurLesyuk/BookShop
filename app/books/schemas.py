from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

GENRES = ["Fiction", "Non-Fiction", "Science", "History"]

class AuthorRead(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    genre: str
    published_year: int
    author_name: str = Field(..., min_length=1)

    @validator("published_year")
    def validate_year(cls, v):
        current_year = datetime.now().year
        if not (1800 <= v <= current_year):
            raise ValueError("published_year must be between 1800 and current year")
        return v

    @validator("genre")
    def validate_genre(cls, v):
        if v not in GENRES:
            raise ValueError(f"Genre must be one of {GENRES}")
        return v

class BookCreate(BookBase):
    pass

class BookRead(BaseModel):
    id: int
    title: str
    genre: str
    published_year: int
    author: AuthorRead

    model_config = {
        "from_attributes": True
    }