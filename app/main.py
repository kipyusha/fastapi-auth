from fastapi import FastAPI
from app.core.database import engine, Base
from contextlib import asynccontextmanager
from app.api.auth import router as page_router
from app.api.admin import router as admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


    

app = FastAPI(lifespan=lifespan)
app.include_router(page_router)
app.include_router(admin_router)

@app.get("/")
async def root():
    return {"status": "ok"}

