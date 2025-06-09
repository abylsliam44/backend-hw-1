from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal

def init_categories(db: Session, user_id: int):
    default_categories = [
        {
            "name": "Salary",
            "description": "Monthly salary and other regular income",
            "color": "#4CAF50",  # Green
            "owner_id": user_id
        },
        {
            "name": "Investments",
            "description": "Investment returns and dividends",
            "color": "#2196F3",  # Blue
            "owner_id": user_id
        },
        {
            "name": "Groceries",
            "description": "Food and household items",
            "color": "#FF9800",  # Orange
            "owner_id": user_id
        },
        {
            "name": "Utilities",
            "description": "Bills for electricity, water, internet, etc.",
            "color": "#F44336",  # Red
            "owner_id": user_id
        },
        {
            "name": "Entertainment",
            "description": "Movies, games, hobbies",
            "color": "#9C27B0",  # Purple
            "owner_id": user_id
        },
        {
            "name": "Transportation",
            "description": "Public transport, fuel, car maintenance",
            "color": "#795548",  # Brown
            "owner_id": user_id
        },
        {
            "name": "Healthcare",
            "description": "Medical expenses and insurance",
            "color": "#607D8B",  # Blue Grey
            "owner_id": user_id
        },
        {
            "name": "Shopping",
            "description": "Clothes, electronics, home items",
            "color": "#E91E63",  # Pink
            "owner_id": user_id
        }
    ]

    for category_data in default_categories:
        db_category = models.Category(**category_data)
        db.add(db_category)
    
    try:
        db.commit()
    except Exception as e:
        print(f"Error adding default categories: {e}")
        db.rollback()

def init_db():
    db = SessionLocal()
    try:
        # Get the first user
        user = db.query(models.User).first()
        if user:
            init_categories(db, user.id)
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 