import pytest
from app.users.models import User
from app.users.auth import get_password_hash, create_access_token
from uuid import uuid4

import random

def generate_phone_number():
    return "+380" + "".join([str(random.randint(0, 9)) for _ in range(9)])

@pytest.mark.asyncio
async def test_register_user(async_client):
    email = f"user_{uuid4().hex[:8]}@example.com"
    phone = generate_phone_number()
    response = await async_client.post("/auth/register/", json={
        "email": email,
        "password": "strongpassword123",
        "phone_number": phone,
        "first_name": "John",
        "last_name": "Doeh"
    })
    print(">>>", response.status_code, response.text)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login_user(async_client, db_session):
    email = f"login_{uuid4().hex[:8]}@example.com"
    phone = generate_phone_number()
    user = User(
        email=email,
        password=get_password_hash("password123"),
        phone_number=phone,
        first_name="Login",
        last_name="Tester"
    )
    db_session.add(user)
    await db_session.commit()

    response = await async_client.post("/auth/login/", json={
        "email": email,
        "password": "password123"
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_current_user(async_client, db_session):
    email = f"me_{uuid4().hex[:8]}@example.com"
    phone = generate_phone_number()
    user = User(
        email=email,
        password=get_password_hash("password"),
        phone_number=phone,
        first_name="Me",
        last_name="User"
    )
    db_session.add(user)
    await db_session.commit()

    token = create_access_token({"sub": str(user.id)})
    async_client.cookies.set("users_access_token", token)

    response = await async_client.get("/auth/me/")
    assert response.status_code == 200
    assert response.json()["email"] == email
