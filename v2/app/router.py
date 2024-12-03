from json import JSONDecodeError
from typing import Annotated, Optional, Literal

from pydantic import ValidationError
from fastapi import APIRouter, Depends
from fastapi.exceptions import RequestValidationError
from sqlalchemy import insert, select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database_depends import get_db
from app.models import Book
from app.schemas import SBooks

app = APIRouter(prefix='/books', tags=['Книги'])

@app.post('/add')
async def add_book(db: Annotated[AsyncSession, Depends(get_db)], book: SBooks):
    try:
        query = insert(Book).values(title=book.title,
                                author=book.author,
                                year=book.year,
                                status=book.status)
        await db.execute(query)
        await db.commit()
        return 'Книга была успешно добавлена'
    except ValidationError as e:
        return 'Вы ввели неверный тип данных'

@app.delete('/delete')
async def delete_book(db: Annotated[AsyncSession, Depends(get_db)], book_id: int):
    result = await db.execute(select(Book).filter_by(id=book_id))
    book = result.scalar_one_or_none()
    if book is not None:
        query = delete(Book).where(Book.id==book_id)
        await db.execute(query)
        await db.commit()
        return 'Книга была успешно удалена'
    else:
        return 'Книга с таким ID отсутствует'


@app.get('/search')
async def book_search(db: Annotated[AsyncSession,Depends(get_db)],criterion: Literal['title','author','year'], value: str):
    if criterion == 'year':
        try:
            value = int(value)
        except ValueError:
            return 'Некорректное значение для года'

    possibilities = {
        'title': Book.title == value,
        'author': Book.author == value,
        'year': Book.year == value
    }
    possibilities_condiotion = possibilities.get(criterion)
    if possibilities_condiotion is None:
        return 'Введен некорректный критерий'
    query = await db.scalars(select(Book).where(possibilities_condiotion))
    return query.all()

@app.get('/get_all')
async def get_all_books(db: Annotated[AsyncSession, Depends(get_db)]):
    query =  await db.scalars(select(Book))
    return query.all()

@app.patch('/update_status')
async def update_book_status(db: Annotated[AsyncSession, Depends(get_db)], book_id: int, new_status: str):
    if new_status in ['в наличии', 'выдана']:
        query = update(Book).where(Book.id==book_id).values(status=new_status)
        await db.execute(query)
        await db.commit()
        return 'Статус был успешно изменен'
    return 'Неверно введен статус'