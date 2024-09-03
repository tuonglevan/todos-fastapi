import uvicorn
from fastapi import FastAPI

from app.routers import router

app = FastAPI(
    title="Todo FastAPI",
    version="1.0.0"
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app)