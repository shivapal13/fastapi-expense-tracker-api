import traceback

try:
    from fastapi import FastAPI
    from app.routers import user, auth, expense

    print("IMPORTS OK")

    app = FastAPI()

    app.include_router(user.router)
    app.include_router(auth.router)
    app.include_router(expense.router)

    print("APP READY")

except Exception:
    traceback.print_exc()