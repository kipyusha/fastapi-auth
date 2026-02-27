from fastapi import FastAPI
from app.core.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


    

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)