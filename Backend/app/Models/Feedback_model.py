from sqlalchemy import String,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column,Relationship

from Backend.app.Models.base_model import BaseModel

class Feedback(BaseModel):
    __tablename__= "Feedback_Table"
    
    message_id: Mapped[int] = mapped_column(
        ForeignKey("Message_Table.id"),
        nullable=False,
        index=True,
    )

    rating: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    message = Relationship("Messages",
                         back_populates="feedbck")

     
