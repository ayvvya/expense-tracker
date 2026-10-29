from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from expense_tracker.database import get_db
from expense_tracker.models import Category, Expense
from expense_tracker.schemas import ExpenseCreate, ExpenseRead

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(data: ExpenseCreate, db: Session = Depends(get_db)):
    if db.get(Category, data.category_id) is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    expense = Expense(**data.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=list[ExpenseRead])
def list_expenses(
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(Expense).order_by(Expense.date.desc(), Expense.id.desc())
    if category_id is not None:
        query = query.where(Expense.category_id == category_id)
    return db.scalars(query).all()


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(Expense, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Расход не найден")

    db.delete(expense)
    db.commit()
