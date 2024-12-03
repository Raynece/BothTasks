from fastapi import FastAPI
from app.router import app as app_books

app = FastAPI()

app.include_router(app_books)