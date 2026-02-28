from pydantic import BaseModel, EmailStr

class RegisterUser(BaseModel):
    name: str
    last_name: str
    middle_name: str
    email: EmailStr
    password: str 
    password_confirm: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    last_name: str
    middle_name: str
    
    class Config:
        from_attributes = True