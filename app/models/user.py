from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import Optional, List
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    subscriptions: Mapped[List["UserSubscription"]] = relationship(
        "UserSubscription", 
        back_populates="user",
        lazy="selectin"
    )
    