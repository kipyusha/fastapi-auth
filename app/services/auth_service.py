from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import hash_password, verify_password

async def register(data, db: AsyncSession):
    if data.password != data.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords mismatch")
    
    res = await db.execute(select(User).where(User.email == data.email))
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email exists")
    hashed_password = hash_password(data.password)
    user = User(
        email = data.email,
        name = data.name,
        password_hash = hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def login(data, db: AsyncSession):
    res = await db.execute(select(User).where(User.email == data.email))
    user = res.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User deleted")
    
    return user