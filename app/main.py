from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, transactions, users, categories
from app import models
from app.database import engine
from app.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Finance API")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(users.router)
app.include_router(categories.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Personal Finance API"} 