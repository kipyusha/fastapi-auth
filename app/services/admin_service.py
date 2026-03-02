from sqlalchemy import select
from fastapi import HTTPException
from app.models.user import User

async def find_user_by_email(email: str, db):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="The user was not found")
    return user

async def change_user_role(email: str, new_role: str, db):
    user = await find_user_by_email(email, db)
    user.role = new_role
    await db.commit()
    await db.refresh(user)

    return user

async def get_all_users(db, skip: int = 0, limit = 100):
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users