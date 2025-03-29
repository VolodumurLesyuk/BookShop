from pydantic import BaseModel, EmailStr, Field, validator
import re


class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Пошта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, від 5 до 50 знаків")
    phone_number: str = Field(..., description="Номер телефону у міжнародному форматі")
    first_name: str = Field(..., min_length=3, max_length=50, description="Ім'я, від 3 до 50  символів")
    last_name: str = Field(..., min_length=3, max_length=50, description="Прізвище, від 3 до 50  символів")

    @validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефону повинен починатись з + і мати від 5 до 15 цифр')
        return value


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Пошта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, від 5 до 50 знаків")


class SUserRole(BaseModel):
    email: EmailStr = Field(..., description="Пошта")
    password: str = Field(...,)
    phone_number: str = Field(..., description="Номер телефону у міжнародному форматі")
    first_name: str = Field(..., min_length=3, max_length=50, description="Ім'я, від 3 до 50  символів")
    last_name: str = Field(..., min_length=3, max_length=50, description="Прізвище, від 3 до 50  символів")
    is_admin: bool= Field(..., description="Користувач адмін?")
    is_user: bool = Field(..., description="Користувач user?")
    is_super_admin: bool = Field(..., description="Користувач super admin?")
