from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db
from app.init_db import init_categories

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=List[schemas.Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    categories = db.query(models.Category).filter(
        models.Category.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    # If user has no categories, initialize default ones
    if not categories:
        init_categories(db, current_user.id)
        categories = db.query(models.Category).filter(
            models.Category.owner_id == current_user.id
        ).offset(skip).limit(limit).all()
    
    return categories

@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_category = models.Category(**category.dict(), owner_id=current_user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.owner_id == current_user.id
    ).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.owner_id == current_user.id
    ).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id,
        models.Category.owner_id == current_user.id
    ).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"} 