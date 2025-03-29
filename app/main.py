from fastapi import FastAPI

from app.users.router import router as router_users
from app.books.router import router as books_router


app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привіт"}

app.include_router(router_users)
app.include_router(books_router)