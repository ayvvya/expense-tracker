from fastapi import FastAPI

from expense_tracker import models  # noqa: F401
from expense_tracker.database import Base, engine
from expense_tracker.routes.budgets import router as budgets_router
from expense_tracker.routes.categories import router as categories_router
from expense_tracker.routes.expenses import router as expenses_router

app = FastAPI(title="Expense Tracker")

Base.metadata.create_all(bind=engine)

app.include_router(categories_router)
app.include_router(expenses_router)
app.include_router(budgets_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
