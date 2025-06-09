from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .models import TransactionType

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None

class Category(CategoryBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float = Field(gt=0)
    type: TransactionType
    description: Optional[str] = None
    category_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    owner_id: int
    created_at: datetime
    category: Category

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    amount: float = Field(gt=0)
    category_id: int
    month: int = Field(ge=1, le=12)
    year: int = Field(ge=2000, le=3000)

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    owner_id: int
    created_at: datetime
    category: Category

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserList(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class CategoryTotal(BaseModel):
    category_id: int
    category_name: str
    total_amount: float
    percentage: float

class MonthlyTotal(BaseModel):
    month: int
    year: int
    income: float
    expenses: float
    savings: float

class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    total_savings: float
    monthly_totals: List[MonthlyTotal]
    top_expense_categories: List[CategoryTotal]
    top_income_categories: List[CategoryTotal]
    budget_status: List[dict] 