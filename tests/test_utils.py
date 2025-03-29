import pytest
import json
from fastapi import UploadFile, HTTPException
from io import BytesIO

from app.books.utils import parse_books_file


class FakeUploadFile(UploadFile):
    def __init__(self, filename: str, content: bytes):
        super().__init__(filename=filename, file=BytesIO(content))


@pytest.mark.asyncio
async def test_parse_json_file_success():
    data = [{"title": "Book1", "author_name": "Author", "published_year": 2020, "genre": "Fiction"}]
    content = bytes(json.dumps(data), "utf-8")
    file = FakeUploadFile("books.json", content)

    parsed = await parse_books_file(file)
    assert parsed == data


@pytest.mark.asyncio
async def test_parse_json_file_invalid():
    file = FakeUploadFile("books.json", b"{invalid json}")

    with pytest.raises(HTTPException) as exc:
        await parse_books_file(file)
    assert exc.value.status_code == 400
    assert "File parsing error" in exc.value.detail


@pytest.mark.asyncio
async def test_parse_csv_file_success():
    content = b"title,author_name,published_year,genre\nBook1,Author,2020,Fiction"
    file = FakeUploadFile("books.csv", content)

    parsed = await parse_books_file(file)
    assert parsed == [{"title": "Book1", "author_name": "Author", "published_year": "2020", "genre": "Fiction"}]


@pytest.mark.asyncio
async def test_parse_csv_file_invalid():
    file = FakeUploadFile("books.csv", b"\xff\xfe\x00\x00")  # явно некоректна кодування

    with pytest.raises(HTTPException) as exc:
        await parse_books_file(file)
    assert exc.value.status_code == 400
    assert "File parsing error" in exc.value.detail


@pytest.mark.asyncio
async def test_parse_unsupported_file_format():
    file = FakeUploadFile("books.txt", b"some content")

    with pytest.raises(HTTPException) as exc:
        await parse_books_file(file)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Unsupported file format"

