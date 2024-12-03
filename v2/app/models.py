from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Integer, String

from app.database import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int]  = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()
