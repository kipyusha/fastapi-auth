
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User
from app.core.database import SessionLocal
from app.models.subscription import UserSubscription, SubscriptionPlan

async def get_db():
    async with SessionLocal() as session:
        yield session


oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2), db = Depends(get_db)):
    
    try:
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    
    return user

async def require_admin(
        current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator rights are required"
        )
    

async def require_subscription_level(
    required_level: int, 
    current_user: User, 
    db: AsyncSession
):

    result = await db.execute(
        select(UserSubscription, SubscriptionPlan)
        .join(SubscriptionPlan, UserSubscription.plan_id == SubscriptionPlan.id)
        .where(
            UserSubscription.user_id == current_user.id,
            UserSubscription.is_active == True
        )
    )
    
    subscription_data = result.first()
    
    if not subscription_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No active subscription found. Level {required_level} required"
        )
    
    subscription, plan = subscription_data

    user_level = 0
    if plan.access_trainer:
        user_level = 3
    elif plan.access_video:
        user_level = 2
    elif plan.access_text:
        user_level = 1
    
    if user_level < required_level:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Subscription level {required_level} required (current: {user_level})"
        )
    
    return current_user

async def require_level_1(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await require_subscription_level(1, current_user, db)

async def require_level_2(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await require_subscription_level(2, current_user, db)

async def require_level_3(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await require_subscription_level(3, current_user, db)