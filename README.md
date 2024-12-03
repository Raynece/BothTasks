
# Library Manager (v1 и v2)

Я решил выполнить это ТЗ двумя разными способами:1)чтобы он соответствовал всем критериям, 2) Чтобы хоть как-то отразить часть моих технических знанний. Этот репозиторий содержит два варианта проекта для управления библиотекой книг. Оба варианта предоставляют функционал для работы с книгами, но реализованы по-разному: первый — с использованием консольного приложения, а второй — через API с использованием FastAPI и базы данных PostgreSQL.

## Проект v1: Консольное приложение для управления библиотекой

Это консольное приложение для управления библиотекой книг. Оно позволяет добавлять, удалять, искать, изменять статус книг и отображать список всех книг в библиотеке.

### Описание функционала

Программа предоставляет функционал для выполнения различных операций с книгами в библиотеке. Каждая книга состоит из следующих атрибутов:

- **id**: Уникальный идентификатор книги (генерируется автоматически).
- **title**: Название книги.
- **author**: Автор книги.
- **year**: Год издания книги.
- **status**: Статус книги. Два возможных значения: `"в наличии"` и `"выдана"`.

#### Основные операции:

1. **Добавление книги**  
   Пользователь может добавить книгу в библиотеку, указав название, автора и год издания. Книга автоматически получит уникальный идентификатор и будет иметь статус `"в наличии"`.
   
2. **Удаление книги**  
   Книга может быть удалена по уникальному идентификатору. Если книга с указанным ID не существует, будет выведено соответствующее сообщение об ошибке.

3. **Поиск книги**  
   Пользователь может искать книги по названию, автору или году издания. Поиск регистронезависимый.

4. **Отображение всех книг**  
   Программа выводит список всех книг в библиотеке с их идентификаторами, названиями, авторами, годами издания и статусами.

5. **Изменение статуса книги**  
   Статус книги можно изменить на `"в наличии"` или `"выдана"`. Если указан неверный статус или книга с данным ID не найдена, будет выведено сообщение об ошибке.

### Структура проекта:

- **library_manager.py**  
  Главный файл с реализацией всех функций программы. Он управляет библиотекой и предоставляет интерфейс командной строки для взаимодействия с пользователем.

- **book.py**  
  Содержит класс `Book`, который представляет книгу с ее аттрибутами: id, title, author, year, status.

- **utils.py**  
  Утилитные функции для работы с файлами (загрузка и сохранение данных о книгах в формате JSON), а также генерация уникальных идентификаторов.

- **data/library_data.json**  
  Файл, который используется для хранения данных о книгах в формате JSON.

- **README.md**  
  Описание проекта, инструкция по использованию и краткое описание функционала.

### Пример использования:

1. При запуске программы пользователю будет предложено меню с доступными операциями:

**Меню**:

- **1. Добавить книгу**
- **2. Удалить книгу**
- **3. Поиск книги**
- **4. Отобразить все книги**
- **5. Изменить статус книги**
- **6. Выход**

2. Для каждой операции будет предложено ввести соответствующие данные (например, для добавления книги — название, автор и год издания).

3. Все изменения сохраняются в файл `data/library_data.json`, чтобы данные сохранялись между запусками программы.

### Хранение данных:

Данные о книгах сохраняются в формате JSON в файле `data/library_data.json`. Этот файл автоматически загружается при запуске программы и обновляется при изменении данных (добавление, удаление, изменение статуса книги).

Пример данных в файле JSON:

```json
[
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "status": "в наличии"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "year": 1960,
        "status": "в наличии"
    },
    {
        "id": 3,
        "title": "Мартин Иден",
        "author": "Джек Лондон",
        "year": 1085,
        "status": "в наличии"
    }
]
```

## Проект v2: API для управления библиотекой через FastAPI

Это приложение для управления библиотекой книг с использованием FastAPI и PostgreSQL. Приложение позволяет добавлять, удалять, искать и отображать книги в библиотеке через API. Каждая книга содержит уникальный идентификатор, название, автора, год издания и статус (в наличии или выдана).

### Описание функционала

#### 1. **Добавление книги**
   Пользователь вводит название книги (`title`), автора (`author`), год издания (`year`), и книга добавляется в библиотеку с уникальным идентификатором и статусом `"в наличии"`.

   **Метод**: `POST /books/add`  
   **Тело запроса**:
   ```json
   {
     "title": "Название книги",
     "author": "Автор книги",
     "year": 2023,
     "status": "в наличии"
   }
   ```

#### 2. **Удаление книги**
   Пользователь вводит уникальный идентификатор книги (`id`), и книга удаляется из библиотеки. Если книги с таким `id` не существует, возвращается ошибка.

   **Метод**: `DELETE /books/delete`  
   **Параметры запроса**:
   ```json
   {
     "book_id": 1
   }
   ```

#### 3. **Поиск книги**
   Пользователь может искать книгу по названию (`title`), автору (`author`) или году издания (`year`).

   **Метод**: `GET /books/search`  
   **Параметры запроса**:
   - `criterion`: критерий поиска, один из следующих: `"title"`, `"author"`, `"year"`
   - `value`: значение для поиска (например, `"название книги"`, `"автор книги"`, `2023`)

   Пример запроса:
   ```bash
   GET /books/search?criterion=title&value=Название книги
   ```

#### 4. **Отображение всех книг**
   Приложение выводит список всех книг в библиотеке с их идентификаторами, названиями, авторами, годами издания и статусами.

   **Метод**: `GET /books/get_all`

#### 5. **Изменение статуса книги**
   Пользователь может изменить статус книги на `"в наличии"` или `"выдана"`.

   **Метод**: `PATCH /books/update_status`  
   **Параметры запроса**:
   ```json
   {
     "book_id": 1,
     "new_status": "выдана"
   }
   ```

---

## Структура проекта v2

```
app/
│
├── config.py               # Конфигурация приложения
├── database.py             # Конфигурация подключения к базе данных (SQLAlchemy)
├── database_depends.py     # Модуль для работы с зависимостями базы данных
├── main.py                 # Основной файл с запуском FastAPI приложения
├── models.py               # Модели SQLAlchemy
├── router.py               # Роутеры (API для работы с книгами)
├── schemas.py              # Схемы Pydantic для валидации данных
└── __init__.py             # Инициализация пакета
alembic.ini                 # Конфигурация Alembic для миграций базы данных
```

### Описание файлов:

1. **`database.py`**: Содержит конфигурацию для подключения к базе данных PostgreSQL с использованием SQLAlchemy.
2. **`database_depends.py`**: Осуществляет зависимость для получения сессии базы данных в запросах FastAPI.
3. **`main.py`**: Основной файл приложения, где создаётся экземпляр FastAPI и подключаются роутеры.
4. **`models.py`**: Определение моделей для работы с таблицами базы данных, в частности, модель `Book` для хранения информации о книгах.
5. **`router.py`**: API для работы с книгами (добавление, удаление, поиск, изменение статуса).
6. **`schemas.py`**: Схемы Pydantic для валидации данных, которые отправляются через API.

---

## Установка и запуск

### Требования:
- Python 3.8+
- PostgreSQL

### Шаги для установки:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Raynece/TestTaskWithFastAPI.git
   cd TestTaskWithFastAPI
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -