from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import RegisterUser, LoginSchema, UserOut, UserUpdate
from app.services.auth_service import login as login_user
from app.services.auth_service import register as register_user
from app.core.security import create_token
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=UserOut)
async def register(data: RegisterUser, db: AsyncSession = Depends(get_db)):
    return await register_user(data, db)

@router.post("/login")
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    user = await login_user(data, db)
    return {"access_token": create_token(user.id)}

@router.get("/me", response_model=UserOut)
async def me(user = Depends(get_current_user)):
    return user

@router.patch("/me")
async def update(data: UserUpdate, user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if data.name:
        user.name = data.name
    await db.commit()
    return user

@router.delete("/me")
async def delete(user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user.is_active = False
    await db.commit()
    return {"detail": "User deactivated"}