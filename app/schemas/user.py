from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

class RegisterUser(BaseModel):
    name: str
    last_name: str
    middle_name: str
    email: EmailStr
    password: str 
    password_confirm: str
    role: UserRole = UserRole.USER

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    role: Optional[UserRole] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    last_name: str
    middle_name: str
    role: UserRole
    
    class Config:
        from_attributes = True