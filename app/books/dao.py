from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.books.models import Book, Author
from app.database import async_session_maker
from app.dao.base import BaseDAO

class AuthorsDAO(BaseDAO):
    model = Author

    @classmethod
    async def get_or_create(cls, name: str) -> Author:
        async with async_session_maker() as session:
            result = await session.execute(select(cls.model).where(cls.model.name == name))
            author = result.scalar_one_or_none()
            if author:
                return author
            new_author = Author(name=name)
            session.add(new_author)
            await session.commit()
            await session.refresh(new_author)
            return new_author

class BooksDAO(BaseDAO):
    model = Book

    @classmethod
    async def get_filtered_books(cls, title=None, author=None, genre=None, year_from=None, year_to=None,
                                 sort_by="title", order="asc", skip=0, limit=10):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(Book.author))

            if title:
                query = query.where(cls.model.title.ilike(f"%{title}%"))
            if author:
                query = query.join(Book.author).where(Author.name.ilike(f"%{author}%"))
            if genre:
                query = query.where(cls.model.genre == genre)
            if year_from:
                query = query.where(cls.model.published_year >= year_from)
            if year_to:
                query = query.where(cls.model.published_year <= year_to)

            sort_column = getattr(cls.model, sort_by if sort_by != "author" else "title")
            query = query.order_by(sort_column.asc() if order == "asc" else sort_column.desc())

            query = query.offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
