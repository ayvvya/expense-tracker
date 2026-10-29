from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from expense_tracker.database import get_db
from expense_tracker.models import Budget, Category, Expense
from expense_tracker.schemas import BudgetRead, BudgetStatus, BudgetUpsert

router = APIRouter(prefix="/budgets", tags=["budgets"])

MONTH_PATTERN = r"^\d{4}-(0[1-9]|1[0-2])$"


def month_range(month: str) -> tuple[date, date]:
    year, mon = map(int, month.split("-"))
    start = date(year, mon, 1)
    end = date(year + 1, 1, 1) if mon == 12 else date(year, mon + 1, 1)
    return start, end


@router.put("", response_model=BudgetRead)
def upsert_budget(data: BudgetUpsert, db: Session = Depends(get_db)):
    if db.get(Category, data.category_id) is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    budget = db.scalar(
        select(Budget).where(
            Budget.category_id == data.category_id,
            Budget.month == data.month,
        )
    )
    if budget is None:
        budget = Budget(
            category_id=data.category_id,
            month=data.month,
            limit_amount=data.limit_amount,
        )
        db.add(budget)
    else:
        budget.limit_amount = data.limit_amount

    db.commit()
    db.refresh(budget)
    return budget


@router.get("/status", response_model=list[BudgetStatus])
def budget_status(
    month: str = Query(pattern=MONTH_PATTERN),
    db: Session = Depends(get_db),
):
    start, end = month_range(month)
    budgets = db.scalars(
        select(Budget).where(Budget.month == month).order_by(Budget.category_id)
    ).all()

    result = []
    for budget in budgets:
        amounts = db.scalars(
            select(Expense.amount).where(
                Expense.category_id == budget.category_id,
                Expense.date >= start,
                Expense.date < end,
            )
        ).all()
        # Суммируем через Decimal, а не через SQL SUM: в SQLite SUM может вернуть float
        spent = sum((Decimal(a) for a in amounts), Decimal("0.00"))
        remaining = budget.limit_amount - spent

        result.append(
            BudgetStatus(
                category_id=budget.category_id,
                category_name=budget.category.name,
                month=month,
                limit_amount=budget.limit_amount,
                spent=spent,
                remaining=remaining,
                exceeded=spent > budget.limit_amount,
            )
        )
    return result
