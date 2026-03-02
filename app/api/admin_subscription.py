from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.deps import get_current_user, require_admin
from app.models.user import User
from app.models.subscription import SubscriptionPlan, UserSubscription
from app.schemas.subscription import (
    UserSubscriptionOut,
    UserSubscriptionAssign
)
from sqlalchemy import select

router = APIRouter(prefix="/admin/subscriptions")

@router.post("/assign", response_model=UserSubscriptionOut)
async def assign_subscription_to_user(
    assignment: UserSubscriptionAssign,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user_result = await db.execute(
        select(User).where(User.id == assignment.user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    plan_result = await db.execute(
        select(SubscriptionPlan).where(SubscriptionPlan.id == assignment.plan_id)
    )
    plan = plan_result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Subscription plan not found")
    
    existing_subscription_result = await db.execute(
        select(UserSubscription)
        .where(
            UserSubscription.user_id == assignment.user_id,
            UserSubscription.is_active == True
        )
    )
    existing_subscription = existing_subscription_result.scalar_one_or_none()
    
    if existing_subscription:
        existing_subscription.is_active = False
        db.add(existing_subscription)
    
    subscription = UserSubscription(
        user_id=assignment.user_id,
        plan_id=assignment.plan_id,
        is_active=True,
    )
    
    db.add(subscription)
    await db.commit()
    
    result = await db.execute(
        select(UserSubscription)
        .where(UserSubscription.id == subscription.id)
        .options(selectinload(UserSubscription.user), selectinload(UserSubscription.plan))
    )
    subscription = result.scalar_one()
    
    return subscription