from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.schemas.user import UserRole, UserOut

class UserSearch(BaseModel):
    email: EmailStr

class UserUpdateRole(BaseModel):
    email: EmailStr
    new_role: UserRole

class UserBulkUpdateRole(BaseModel):
    emails: List[EmailStr]
    new_role: UserRole

class UserDeactivate(BaseModel):
    email: EmailStr
    is_active: bool = False

class UserSearchResult(BaseModel):
    users: List[UserOut]
    total: int