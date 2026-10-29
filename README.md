# Expense Tracker

REST API для учёта расходов и контроля месячных бюджетов по категориям.

![tests](https://github.com/ayvvya/expense-tracker/actions/workflows/ci.yml/badge.svg)

## Возможности

- Категории расходов с защитой от дубликатов
- Учёт расходов с фильтрацией по категории
- Месячные бюджеты для каждой категории
- Отчёт `GET /budgets/status`: потрачено, остаток и превышение лимита

## Стек

Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, SQLite, pytest, Docker

## Запуск локально

```bash
uv sync
uv run uvicorn expense_tracker.main:app --reload
```

Документация API: http://127.0.0.1:8000/docs

## Тесты

```bash
uv run pytest
```

## Структура

```
src/expense_tracker/
├── main.py        # создание приложения
├── models.py      # таблицы SQLAlchemy
├── schemas.py     # схемы запросов и ответов
├── database.py    # подключение к базе
└── routes/        # эндпоинты
tests/             # автотесты
```
