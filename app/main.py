from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.database import Base,engine
from app import models
from app.routers import expense
from app.routers import user
from app.routers import auth

app=FastAPI()

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)




app.include_router(expense.router)
app.include_router(user.router)
app.include_router(auth.router)


