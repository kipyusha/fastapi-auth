from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.subscription import SubscriptionPlan, UserSubscription

from app.schemas.subscription import UserAccessInfo



async def get_subscription_plans(db):
    result = await db.execute(select(SubscriptionPlan))
    plans = result.scalars().all()
    return plans

async def assign_subscription_to_user(db, user_id: int, plan_id: int):
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    plan_result = await db.execute(select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id))
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    
    old_subs_result = await db.execute(
        select(UserSubscription).where(
            UserSubscription.user_id == user_id,
            UserSubscription.is_active == True
        )
    )
    old_subs = old_subs_result.scalars().all()
    for sub in old_subs:
        sub.is_active = False
        await db.commit()
    
    subscription = UserSubscription(
        user_id=user_id,
        plan_id=plan_id,
        is_active=True,
    )
    
    db.add(subscription)
    await db.commit()
    await db.refresh(subscription)
    
    return subscription

async def check_user_access(user_id: int, db: AsyncSession) -> UserAccessInfo:
    result = await db.execute(
        select(UserSubscription, SubscriptionPlan)
        .join(SubscriptionPlan, UserSubscription.plan_id == SubscriptionPlan.id)
        .where(
            UserSubscription.user_id == user_id,
            UserSubscription.is_active == True
        )
    )
    
    subscription_data = result.first()
    
    if not subscription_data:
        return UserAccessInfo(
            has_access_text=False,
            has_access_video=False,
            has_access_trainer=False,
            subscription_level=None,
            current_plan=None
        )
    
    subscription, plan = subscription_data
    subscription_level = None
    if plan.access_trainer:
        subscription_level = 3
    elif plan.access_video:
        subscription_level = 2
    elif plan.access_text:
        subscription_level = 1
    
    return UserAccessInfo(
        has_access_text=plan.access_text,
        has_access_video=plan.access_video,
        has_access_trainer=plan.access_trainer,
        subscription_level=subscription_level,
        current_plan=plan.name
    )

async def get_user_subscription_info(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(UserSubscription, SubscriptionPlan)
        .join(SubscriptionPlan, UserSubscription.plan_id == SubscriptionPlan.id)
        .where(
            UserSubscription.user_id == user_id,
            UserSubscription.is_active == True
        )
    )
    
    subscription_data = result.first()
    
    if not subscription_data:
        return None
    
    subscription, plan = subscription_data
    
    return {
        "subscription_id": subscription.id,
        "plan_id": plan.id,
        "plan_name": plan.name,
        "plan_description": plan.description,
        "access_text": plan.access_text,
        "access_video": plan.access_video,
        "access_trainer": plan.access_trainer,
        "is_active": subscription.is_active,
        "created_at": subscription.created_at if hasattr(subscription, 'created_at') else None,
        "expires_at": subscription.expires_at if hasattr(subscription, 'expires_at') else None
    }

async def get_all_user_subscriptions(user_id: int, db: AsyncSession):
    result = await db.execute(
        select(UserSubscription, SubscriptionPlan)
        .join(SubscriptionPlan, UserSubscription.plan_id == SubscriptionPlan.id)
        .where(UserSubscription.user_id == user_id)
        .order_by(UserSubscription.created_at.desc() if hasattr(UserSubscription, 'created_at') else UserSubscription.id.desc())
    )
    
    subscriptions = []
    for subscription, plan in result.all():
        subscriptions.append({
            "subscription_id": subscription.id,
            "plan_id": plan.id,
            "plan_name": plan.name,
            "is_active": subscription.is_active,
            "created_at": subscription.created_at if hasattr(subscription, 'created_at') else None,
            "expires_at": subscription.expires_at if hasattr(subscription, 'expires_at') else None
        })
    
    return subscriptions