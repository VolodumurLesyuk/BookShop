from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime
import csv, json
from sqlalchemy.orm import selectinload
from app.books.models import Book

from app.users.dependencies import get_current_user
from app.books.schemas import BookCreate, BookRead
from app.books.dao import BooksDAO, AuthorsDAO
from app.books.exceptions import BookAlreadyExistsException, FileParseException
from app.users.models import User

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookRead)
async def create_book(book: BookCreate, user: User = Depends(get_current_user)):
    author = await AuthorsDAO.get_or_create(book.author_name)
    try:
        new_book = await BooksDAO.add(
            title=book.title,
            genre=book.genre,
            published_year=book.published_year,
            author_id=author.id
        )
        return await BooksDAO.find_one_or_none_by_id(new_book.id, options=[selectinload(Book.author)])
    except IntegrityError:
        raise BookAlreadyExistsException


@router.get("/", response_model=List[BookRead])
async def get_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    sort_by: Optional[str] = Query("title", enum=["title", "published_year", "author"]),
    order: Optional[str] = Query("asc", enum=["asc", "desc"]),
    skip: int = 0,
    limit: int = 10
):
    return await BooksDAO.get_filtered_books(
        title=title,
        author=author,
        genre=genre,
        year_from=year_from,
        year_to=year_to,
        sort_by=sort_by,
        order=order,
        skip=skip,
        limit=limit
    )


@router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(book_id: int):
    from sqlalchemy.orm import selectinload
    from app.books.models import Book
    book = await BooksDAO.find_one_or_none_by_id(book_id, options=[selectinload(Book.author)])
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookRead)
async def update_book(book_id: int, book: BookCreate, user: User = Depends(get_current_user)):
    from sqlalchemy.orm import selectinload
    from app.books.models import Book

    author = await AuthorsDAO.get_or_create(book.author_name)
    updated = await BooksDAO.update(
        {"id": book_id},
        title=book.title,
        genre=book.genre,
        published_year=book.published_year,
        author_id=author.id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return await BooksDAO.find_one_or_none_by_id(book_id, options=[selectinload(Book.author)])


@router.delete("/{book_id}")
async def delete_book(book_id: int, user: User = Depends(get_current_user)):
    deleted = await BooksDAO.delete(id=book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}


@router.post("/import")
async def import_books(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    from app.books.utils import parse_books_file

    try:
        books_data = await parse_books_file(file)
    except Exception as e:
        raise FileParseException

    added_books = []
    for data in books_data:
        author = await AuthorsDAO.get_or_create(data["author_name"])
        book = await BooksDAO.add(
            title=data["title"],
            genre=data["genre"],
            published_year=int(data["published_year"]),
            author_id=author.id
        )
        added_books.append(book)

    return {"imported": len(added_books)}