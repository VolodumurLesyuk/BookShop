from datetime import datetime, timezone, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import get_auth_data
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encoded_jwt

def create_access_token(data: dict) -> str:
    return create_token(data, expires_delta=timedelta(minutes=60))  # або як тобі треба

def create_refresh_token(data: dict) -> str:
    return create_token(data, expires_delta=timedelta(days=30))  # або більше



async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user