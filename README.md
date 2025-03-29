# 📚 Book Management API

FastAPI-проєкт для управління книгами з авторизацією користувачів, імпортом даних із JSON/CSV, фільтрацією, сортуванням та багато іншого.

---

## 🔧 Технології

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- Alembic
- Pydantic
- httpx + pytest (тестування)

---

## 📦 Встановлення

```bash
git clone git@github.com:VolodumurLesyuk/BookShop.git
cd BookShop
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ⚙️ Налаштування

Створи .env файл:
```commandline
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test_db
DB_USER=admin
DB_PASSWORD=admin
SECRET_KEY=gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt
ALGORITHM=HS256
```

## 🗄️ База даних
Створення та міграція
```
alembic revision --autogenerate -m "init"
alembic upgrade head
```

## 🚀 Запуск сервера
```
uvicorn app.main:app --reload
```

## 🧪 Тестування
```pytest```

## 📚 API Ендпоінти

## 🔐 Авторизація

```
POST /auth/register/ — реєстрація користувача

POST /auth/login/ — логін, повертає access/refresh токени через кукі

GET /auth/me — отримати поточного користувача
```

## 📘 Книги
## 🔐 Потребують авторизації
```
POST /books/ — створити книгу

GET /books/ — отримати всі книги з фільтрацією, сортуванням, пагінацією

GET /books/{id} — отримати книгу за ID

PUT /books/{id} — оновити книгу

DELETE /books/{id} — видалити книгу
```

## 📥 Імпорт книг
```
POST /books/import — завантаження книг із .json або .csv
```

## 🧠 Додаткові можливості
- Авторизація через JWT у куках

- Захист ендпоінтів за допомогою Depends

- Автоматичні тести: API, утиліти

- Парсинг файлів з помилками

- Валідація email, телефону, імені та пароля
