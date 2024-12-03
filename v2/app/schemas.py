from pydantic import BaseModel, Field


class SBooks(BaseModel):
    title: str
    author: str
    year: int
    status: str

