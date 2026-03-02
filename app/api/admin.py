from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.deps import require_admin
from app.services.admin_service import change_user_role, get_all_users, find_user_by_email
from app.schemas.user import UserOut, ChangeRoleRequest
from app.models.user import User

router = APIRouter(prefix="/admin")

@router.get("/users", response_model=List[UserOut])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    users = await get_all_users(db, skip, limit)
    return users

@router.get("/user/{email}", response_model=UserOut)
async def get_user(
    email: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = await find_user_by_email(email, db)
    return user

@router.patch("/user/role", response_model=UserOut)
async def update_role(
    data: ChangeRoleRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin)
):
    user = await change_user_role(data.email, data.new_role, db)
    return user