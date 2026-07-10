from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from Backend.app.Models.base_model import BaseModel

class Conversation(BaseModel):
    
    __tablename__ = "Conversation_Table"
    
    title : Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True,
    )  
    
    user_id : Mapped[int] = mapped_column(
        ForeignKey("Users_Table.id"),
        nullable=False,
        index=True,
    )
    # 1 user have many conversations
    user=relationship("User",back_populates="conversations",)
    # 1 conversation has many messages
    messages=relationship("Messages",back_populates="conversations")
    
    