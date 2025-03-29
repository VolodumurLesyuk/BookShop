import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.database import async_session_maker
from app.users.models import User
from app.users.auth import get_password_hash

import uuid

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    return asyncio.new_event_loop()

@pytest.fixture(scope="function")
async def db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

@pytest.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app, raise_app_exceptions=True)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="function")
async def authorized_client(async_client: AsyncClient, db_session: AsyncSession):
    # Генеруємо тестовий email
    email = f"test{str(uuid.uuid4().int)[:9]}@example.com"
    password = "testpassword"

    # Створюємо користувача
    user = User(
        email=email,
        password=get_password_hash(password),
        phone_number=f"+380{str(uuid.uuid4().int)[:9]}",
        first_name="Adddd",
        last_name="AAAAAAAAAAA",
    )
    db_session.add(user)
    await db_session.commit()

    # Логінимося цим користувачем
    response = await async_client.post("/auth/login/", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200, f"Login failed: {response.text}"
    async_client.cookies = response.cookies
    return async_client