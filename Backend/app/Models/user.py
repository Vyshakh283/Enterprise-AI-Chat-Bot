from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from Backend.app.Models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "Users_Table"
    
    username : Mapped[String]=mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    
    email : Mapped[String]=mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    
    hashed_password : Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    
    role : Mapped[str] = mapped_column(
        String(50),
        default="user",
        nullable=False,
    )
    # conversations done by 1 user
    conversations= relationship("Conversation",back_populates="user",cascade="all, delete-orphan",)
    # relationship between document and the user
    document=relationship("Document",back_populates="user")
    
    audit_logs = relationship(
    "AuditLog",
    back_populates="user",
    cascade="all, delete-orphan",
)
    
    
    
    