from fastapi import FastAPI
from contextlib import asynccontextmanager
from wdq.app.core import config, logging
from wdq.app.db.database import init_db
from wdq.app.routers.v1 import users, items

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.setup_logging()
    await init_db()
    yield

app = FastAPI(
    title="my_fastapi_project",
    version="0.1.0",
    description="A FastAPI project",
    lifespan=lifespan
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to my_fastapi_project!"}