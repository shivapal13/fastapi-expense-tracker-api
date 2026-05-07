from fastapi import FastAPI
from app.routers import user, auth, expense
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(expense.router)