from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.subscription import SubscriptionPlan


async def seed_subscription_plans(db: AsyncSession):
    
    plans = [
        {
            "name": "Basic (Level 1)",
            "description": "Доступ к текстовым материалам",
            "access_text": True,
            "access_video": False,
            "access_trainer": False
        },
        {
            "name": "Pro (Level 2)",
            "description": "Доступ к текстовым материалам и видео",
            "access_text": True,
            "access_video": True,
            "access_trainer": False
        },
        {
            "name": "Premium (Level 3)",
            "description": "Полный доступ: текст, видео и тренажеры",
            "access_text": True,
            "access_video": True,
            "access_trainer": True
        }
    ]
    
    for plan_data in plans:
        existing = await db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.name == plan_data["name"])
        )
        existing_plan = existing.scalar_one_or_none()
        
        if not existing_plan:
            plan = SubscriptionPlan(**plan_data)
            db.add(plan)

    await db.commit()