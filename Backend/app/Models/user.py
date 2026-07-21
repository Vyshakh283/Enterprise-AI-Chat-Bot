from datetime import datetime

from sqlalchemy import String,Boolean,Integer,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from Backend.app.Models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "Users_Table"
    
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(30),
        default="USER",
        nullable=False,
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_locked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # conversations done by 1 user
    conversations= relationship("Conversation",back_populates="user",cascade="all, delete-orphan",)
    
    # relationship between document and the user
    document=relationship("Document",back_populates="user")
    
    # relationship between document and the user
    audit_logs = relationship(
    "AuditLog",
    back_populates="user",
    cascade="all, delete-orphan",
)
    
    
    
    