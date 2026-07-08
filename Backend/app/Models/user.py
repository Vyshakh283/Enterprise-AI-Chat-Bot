from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from Backend.app.Models.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "Users"
    
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
    
    