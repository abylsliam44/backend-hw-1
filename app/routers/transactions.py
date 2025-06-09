from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.get("/", response_model=List[schemas.Transaction])
def read_transactions(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.owner_id == current_user.id
    ).order_by(models.Transaction.date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.post("/", response_model=schemas.Transaction)
def create_transaction(
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    # Verify category exists and belongs to user
    category = db.query(models.Category).filter(
        models.Category.id == transaction.category_id,
        models.Category.owner_id == current_user.id
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found or does not belong to user"
        )

    db_transaction = models.Transaction(**transaction.dict(), owner_id=current_user.id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(
    transaction_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id
    ).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id
    ).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Verify category exists and belongs to user
    if transaction.category_id:
        category = db.query(models.Category).filter(
            models.Category.id == transaction.category_id,
            models.Category.owner_id == current_user.id
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found or does not belong to user"
            )
    
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id
    ).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"} 