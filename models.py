from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

class budget(Base):
    __tablename__ = 'budgets'

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