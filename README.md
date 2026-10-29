**Демо:** https://expense-tracker-8y99.onrender.com/docs
# Expense Tracker

REST API для учёта расходов и контроля месячных бюджетов по категориям.

![CI](https://github.com/ayvvya/expense-tracker/actions/workflows/ci.yml/badge.svg)

## Возможности

- Категории расходов с защитой от дубликатов
- Учёт расходов с фильтрацией по категории и датой
- Месячные бюджеты для каждой категории
- Отчёт `GET /budgets/status`: потрачено, остаток и превышение лимита
- Автотесты (pytest) и проверка кода линтером (Ruff) в CI

## Стек

Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, SQLite, pytest, Ruff, Docker, GitHub Actions

## Запуск через Docker

```bash
docker compose up --build
```

Документация API: http://127.0.0.1:8000/docs

## Запуск без Docker

```bash
uv sync
uv run uvicorn expense_tracker.main:app --reload
```

## Пример использования

Установить бюджет на категорию 1 за октябрь 2026:

```bash
curl -X PUT http://127.0.0.1:8000/budgets \
  -H "Content-Type: application/json" \
  -d '{"category_id": 1, "month": "2026-10", "limit_amount": "5000.00"}'
```

Получить отчёт по бюджетам за месяц:

```bash
curl "http://127.0.0.1:8000/budgets/status?month=2026-10"
```

Пример ответа:

```json
[
  {
    "category_id": 1,
    "category_name": "Продукты",
    "month": "2026-10",
    "limit_amount": "5000.00",
    "spent": "3250.50",
    "remaining": "1749.50",
    "exceeded": false
  }
]
```

## Проверки

```bash
uv run pytest          # тесты
uv run ruff check .    # линтер
uv run ruff format .   # форматирование
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
