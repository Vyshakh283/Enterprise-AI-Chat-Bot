from sqlalchemy.orm import mapped_column,Mapped,Relationship
from sqlalchemy import String,ForeignKey,Text

from Backend.app.Models.base_model import BaseModel

class Messages(BaseModel):
    __tablename__ = "Message_Table"
    
    conversation_id : Mapped[int] = mapped_column(
        ForeignKey("Conversation_Table.id"),
        index=True,
        nullable=False,
    )
    
    role : Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
    )
    
    content_messages : Mapped[str] = mapped_column(
        Text,
        index=True,
        nullable=False,
    )
    # many messages has 1 conversations 
    conversations=Relationship("Conversation",back_populates="messages")
