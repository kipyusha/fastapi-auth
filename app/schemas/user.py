from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    email: EmailStr
    name: str
    password: str 
    password_confirm: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    token: str
    name: str

class UserUpdate(BaseModel):
    name: str | None = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    
    class Config:
        from_attributes = True