from sqlalchemy import Boolean, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from app.core.database import Base



class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(String)

    access_text: Mapped[bool] = mapped_column(Boolean, default=False)
    access_video: Mapped[bool] = mapped_column(Boolean, default=False)
    access_trainer: Mapped[bool] = mapped_column(Boolean, default=False)

    user_subscriptions = relationship("UserSubscription", back_populates="plan")

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey("subscription_plans.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default = False)
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan")
    