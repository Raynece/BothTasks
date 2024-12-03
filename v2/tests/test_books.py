import sys
import os

from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем корневую директорию проекта в sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.future import select
from app.models import Book


@pytest.mark.asyncio
async def test_add_book(db_session: AsyncSession, client: TestClient):
    response = client.post("/books/add", json={
        "title": "Тестовая книга",
        "author": "Тестовый автор",
        "year": 2023,
        "status": "в наличии"
    })
    assert response.status_code == 200
    assert response.json() == "Книга была успешно добавлена"

    # Проверяем, что книга добавлена в базу данных
    result = await db_session.execute(select(Book).filter(Book.title == "Тестовая книга"))
    book = result.scalar_one_or_none()
    assert book is not None
    assert book.title == "Тестовая книга"
    assert book.author == "Тестовый автор"
    assert book.year == 2023
    assert book.status == "в наличии"


@pytest.mark.asyncio
async def test_search_book_by_title(db_session: AsyncSession, client: TestClient):
    # Добавляем книгу для поиска
    new_book = Book(title="Книга для поиска", author="Автор поиска", year=2023, status="в наличии")
    db_session.add(new_book)
    await db_session.commit()

    # Ищем книгу по названию
    response = client.get("/books/search?criterion=title&value=Книга для поиска")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["title"] == "Книга для поиска"


@pytest.mark.asyncio
async def test_delete_book(db_session: AsyncSession, client: TestClient):
    # Добавляем книгу для удаления
    new_book = Book(title="Книга для удаления", author="Автор", year=2022, status="в наличии")
    db_session.add(new_book)
    await db_session.commit()

    book_id = new_book.id
    response = client.delete(f"/books/delete?book_id={book_id}")
    assert response.status_code == 200
    assert response.json() == "Книга была успешно удалена"

    # Проверяем, что книга была удалена
    result = await db_session.execute(select(Book).filter(Book.id == book_id))
    deleted_book = result.scalar_one_or_none()
    assert deleted_book is None


@pytest.mark.asyncio
async def test_update_book_status(db_session: AsyncSession, client: TestClient):
    # Добавляем книгу для изменения статуса
    new_book = Book(title="Книга для изменения статуса", author="Автор", year=2022, status="в наличии")
    db_session.add(new_book)
    await db_session.commit()

    book_id = new_book.id
    response = client.patch("/books/update_status", json={
        "book_id": book_id,
        "new_status": "выдана"
    })
    assert response.status_code == 200
    assert response.json() == "Статус был успешно изменен"

    # Проверяем, что статус был изменен
    result = await db_session.execute(select(Book).filter(Book.id == book_id))
    updated_book = result.scalar_one_or_none()
    assert updated_book.status == "выдана"


@pytest.mark.asyncio
async def test_get_all_books(db_session: AsyncSession, client: TestClient):
    # Добавляем книги
    db_session.add(Book(title="Книга 1", author="Автор 1", year=2020, status="в наличии"))
    db_session.add(Book(title="Книга 2", author="Автор 2", year=2021, status="выдана"))
    await db_session.commit()

    response = client.get("/books/get_all")
    assert response.status_code == 200
    books = response.json()
    books = response.json()
    assert len(books) >= 2
    assert books[0]["title"] == "Книга 1"
    assert books[1]["title"] == "Книга 2"

