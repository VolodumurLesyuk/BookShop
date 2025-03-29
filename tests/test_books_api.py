import pytest

@pytest.mark.asyncio
async def test_create_book(authorized_client):
    response = await authorized_client.post("/books/", json={
        "title": "Book Title",
        "author_name": "John Doe",
        "published_year": 2020,
        "genre": "Fiction"
    })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_all_books(authorized_client):
    response = await authorized_client.get("/books/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_book_by_id(authorized_client):
    response = await authorized_client.get("/books/1")
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_update_book(authorized_client):
    response = await authorized_client.put("/books/1", json={
        "title": "Updated Title",
        "author_name": "John Doe",
        "published_year": 2022,
        "genre": "Fiction"
    })
    assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_delete_book(authorized_client):
    response = await authorized_client.delete("/books/1")
    assert response.status_code in [204, 404]
