# main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from routes.budgets import router as budget_router
from routes.users import router as user_router

# Create a FastAPI instance
app = FastAPI()

# Include user and budget routers
app.include_router(user_router)
app.include_router(budget_router)

# Create tables in the database
Base.metadata.create_all(bind=engine)


# Redirect the root URL to the documentation
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
