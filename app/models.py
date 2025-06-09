from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # New field for admin users
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    transactions = relationship("Transaction", back_populates="owner")
    categories = relationship("Category", back_populates="owner")
    budgets = relationship("Budget", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    color = Column(String, default="#000000")  # For UI purposes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    owner = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(Enum(TransactionType))
    description = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    owner = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    month = Column(Integer)  # 1-12
    year = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets") 