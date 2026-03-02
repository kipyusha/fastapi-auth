from pydantic import BaseModel, EmailStr, field_validator


class RegisterUser(BaseModel):
    name: str
    last_name: str
    middle_name: str
    email: EmailStr
    password: str 
    password_confirm: str
    role: str = "user"

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    role: str = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    last_name: str
    middle_name: str
    role: str
    
    class Config:
        from_attributes = True

class ChangeRoleRequest(BaseModel):
    email: EmailStr
    new_role: str
    @field_validator('new_role')
    def validate_role(cls, v):
        allowed = ["user", "manager", "admin"]
        if v not in allowed:
            raise ValueError(f'The role must be: {allowed}')
        return v