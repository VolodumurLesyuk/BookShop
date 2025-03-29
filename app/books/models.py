from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, int_pk, created_at, updated_at

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int_pk]
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    published_year: Mapped[int] = mapped_column(Integer, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author: Mapped[Author] = relationship("Author", back_populates="books")

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]