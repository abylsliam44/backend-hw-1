from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@router.get("/", response_model=List[schemas.UserList])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user is admin (you can modify this based on your needs)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/me/transactions", response_model=List[schemas.Transaction])
def read_user_transactions(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    transactions = db.query(models.Transaction)\
        .filter(models.Transaction.owner_id == current_user.id)\
        .offset(skip).limit(limit).all()
    return transactions

@router.get("/me/categories", response_model=List[schemas.Category])
def read_user_categories(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.categories

@router.get("/me/budgets", response_model=List[schemas.Budget])
def read_user_budgets(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.budgets

@router.get("/me/dashboard", response_model=schemas.DashboardSummary)
def get_dashboard_summary(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Get all user transactions
    transactions = db.query(models.Transaction)\
        .filter(models.Transaction.owner_id == current_user.id).all()
    
    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.type == models.TransactionType.INCOME)
    total_expenses = sum(t.amount for t in transactions if t.type == models.TransactionType.EXPENSE)
    total_savings = total_income - total_expenses

    # Get category totals
    category_totals = {}
    for transaction in transactions:
        if transaction.category_id not in category_totals:
            category_totals[transaction.category_id] = {
                "category_name": transaction.category.name,
                "total_amount": 0,
                "type": transaction.type
            }
        category_totals[transaction.category_id]["total_amount"] += transaction.amount

    # Calculate percentages and create category total objects
    expense_categories = []
    income_categories = []
    for cat_id, data in category_totals.items():
        total = total_expenses if data["type"] == models.TransactionType.EXPENSE else total_income
        if total > 0:
            percentage = (data["total_amount"] / total) * 100
        else:
            percentage = 0
            
        category_total = schemas.CategoryTotal(
            category_id=cat_id,
            category_name=data["category_name"],
            total_amount=data["total_amount"],
            percentage=percentage
        )
        
        if data["type"] == models.TransactionType.EXPENSE:
            expense_categories.append(category_total)
        else:
            income_categories.append(category_total)

    # Sort categories by amount
    expense_categories.sort(key=lambda x: x.total_amount, reverse=True)
    income_categories.sort(key=lambda x: x.total_amount, reverse=True)

    return schemas.DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        total_savings=total_savings,
        monthly_totals=[],  # TODO: Implement monthly breakdown
        top_expense_categories=expense_categories[:5],  # Top 5 expense categories
        top_income_categories=income_categories[:5],    # Top 5 income categories
        budget_status=[]    # TODO: Implement budget status
    ) 