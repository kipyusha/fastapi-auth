from pydantic import BaseModel
from typing import Optional

class SubscriptionPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    access_text: bool = False
    access_video: bool = False
    access_trainer: bool = False

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanOut(SubscriptionPlanBase):
    id: int
    
    class Config:
        from_attributes = True

class UserSubscriptionAssign(BaseModel):
    user_id: int
    plan_id: int

class UserSubscriptionBase(BaseModel):
    user_id: int
    plan_id: int
    is_active: bool = True

class UserSubscriptionCreate(UserSubscriptionBase):
    pass

class UserSubscriptionOut(UserSubscriptionBase):
    id: int
    plan: Optional[SubscriptionPlanOut] = None
    
    class Config:
        from_attributes = True

class UserAccessInfo(BaseModel):
    has_access_text: bool
    has_access_video: bool
    has_access_trainer: bool
    subscription_level: Optional[int]
    current_plan: Optional[str]