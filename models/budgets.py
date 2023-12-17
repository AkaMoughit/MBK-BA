# models/budgets.py
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class Budget(Base):
    # Database table name
    __tablename__ = "budgets"

    # Columns in the 'budgets' table
    budget_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    budget_name = Column(String(255))
    amount = Column(Integer)
    remaining_amount = Column(Integer)
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class BudgetBase(BaseModel):
    # Pydantic model for request input validation
    user_id: int
    budget_name: str
    amount: int = 0
    remaining_amount: int = 0
    start_at: datetime
    end_at: datetime
    created_at: datetime