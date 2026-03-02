from fastapi import FastAPI
from app.core.database import engine, Base, SessionLocal
from contextlib import asynccontextmanager
from app.api.auth import router as page_router
from app.api.admin import router as admin_router
from app.api.content import router as content_router
from app.api.admin_subscription import router as admin_subscription_router
from app.core.seed_subscription_plans import seed_subscription_plans
from app.models.user import User
from app.models.subscription import SubscriptionPlan, UserSubscription
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        async with SessionLocal() as db:
            await seed_subscription_plans(db)
            logger.info("Начальные данные успешно загружены")
    except Exception as e:
        logger.error(f"Ошибка при заполнении базы данных: {e}")
        

    yield


    

app = FastAPI(lifespan=lifespan)
app.include_router(page_router)
app.include_router(admin_router)
app.include_router(content_router)
app.include_router(admin_subscription_router)

@app.get("/")
async def root():
    return {"status": "ok"}

