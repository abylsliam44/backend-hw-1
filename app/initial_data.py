from .database import SessionLocal
from . import models

default_categories = [
    {"name": "Salary", "color": "#4CAF50", "description": "Regular income from employment"},
    {"name": "Freelance", "color": "#81C784", "description": "Income from freelance work"},
    {"name": "Investments", "color": "#66BB6A", "description": "Income from investments"},
    {"name": "Rent/Mortgage", "color": "#F44336", "description": "Housing expenses"},
    {"name": "Groceries", "color": "#2196F3", "description": "Food and household items"},
    {"name": "Utilities", "color": "#FF9800", "description": "Electricity, water, gas, etc."},
    {"name": "Transportation", "color": "#9C27B0", "description": "Public transport, fuel, car maintenance"},
    {"name": "Entertainment", "color": "#E91E63", "description": "Movies, dining out, hobbies"},
    {"name": "Healthcare", "color": "#00BCD4", "description": "Medical expenses and insurance"},
    {"name": "Education", "color": "#009688", "description": "Courses, books, training"},
]

def init_db():
    db = SessionLocal()
    try:
        # Check if we already have categories
        existing_categories = db.query(models.Category).first()
        if not existing_categories:
            for category in default_categories:
                db_category = models.Category(**category)
                db.add(db_category)
            db.commit()
    finally:
        db.close() 