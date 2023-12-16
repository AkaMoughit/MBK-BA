from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class BudgetBase(BaseModel):
    user_id: int
    budget_name: str
    amount: int = 0
    remaining_amount: int = 0
    start_at: datetime
    end_at: datetime
    created_at: datetime

class UserBase(BaseModel):
    username: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    created_at: datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["created_at"] = datetime.now()
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.get("/users/", status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/budgets/", status_code=status.HTTP_201_CREATED)
async def create_budget(budget: BudgetBase, db: Session = Depends(get_db)):
    budget_data = budget.dict()
    budget_data["created_at"] = datetime.now()
    db_budget = models.budget(**budget_data)
    db.add(db_budget)
    db.commit()
    return {"message": "Budget created successfully"}

@app.get("/budgets/{budget_id}", status_code=status.HTTP_200_OK)
async def get_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(models.budget).filter(models.budget.budget_id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget

@app.get("/budgets/", status_code=status.HTTP_200_OK)
async def get_budgets(db: Session = Depends(get_db)):
    budgets = db.query(models.budget).all()
    return budgets