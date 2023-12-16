from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.openapi.models import Info, ExternalDocumentation
from fastapi.responses import RedirectResponse

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
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
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

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    user_data = user.dict()
    user_data["created_at"] = datetime.now()
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user.username = user_data["username"]
    db_user.email = user_data["email"]
    db_user.password_hash = user_data["password_hash"]
    db_user.first_name = user_data["first_name"]
    db_user.last_name = user_data["last_name"]
    db_user.date_of_birth = user_data["date_of_birth"]
    db_user.created_at = user_data["created_at"]
    db.commit()
    return {"message": "User updated successfully"}

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

@app.delete("/budgets/{budget_id}", status_code=status.HTTP_200_OK)
async def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    budget = db.query(models.budget).filter(models.budget.budget_id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}

@app.put("/budgets/{budget_id}", status_code=status.HTTP_200_OK)
async def update_budget(budget_id: int, budget: BudgetBase, db: Session = Depends(get_db)):
    budget_data = budget.dict()
    budget_data["created_at"] = datetime.now()
    db_budget = db.query(models.budget).filter(models.budget.budget_id == budget_id).first()
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    db_budget.user_id = budget_data["user_id"]
    db_budget.budget_name = budget_data["budget_name"]
    db_budget.amount = budget_data["amount"]
    db_budget.remaining_amount = budget_data["remaining_amount"]
    db_budget.start_at = budget_data["start_at"]
    db_budget.end_at = budget_data["end_at"]
    db_budget.created_at = budget_data["created_at"]
    db.commit()
    return {"message": "Budget updated successfully"}