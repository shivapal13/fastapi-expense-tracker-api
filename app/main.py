from dotenv import load_dotenv
load_dotenv()
import traceback

try:
    print("APP STARTING...")
except Exception:
    traceback.print_exc()

try:
    from fastapi import FastAPI 
    from app import models
    from app.routers import expense, user, auth
    print("IMPORTS OK")
except Exception:
    traceback.print_exc()

app=FastAPI()

#models.Base.metadata.create_all(bind=engine)




app.include_router(expense.router)
app.include_router(user.router)
app.include_router(auth.router)


