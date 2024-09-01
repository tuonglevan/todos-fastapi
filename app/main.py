from fastapi import FastAPI

from app.routers import auth, company, user, task

app = FastAPI()

app.include_router(auth.router)
app.include_router(company.router)
app.include_router(user.router)
app.include_router(task.router)