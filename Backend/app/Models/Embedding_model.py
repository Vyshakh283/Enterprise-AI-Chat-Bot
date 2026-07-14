from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped,mapped_column,relationship
from Backend.app.Models.base_model import BaseModel
from pgvector.sqlalchemy import Vector

class Embedding(BaseModel):
    __tablename__="Embedding_Table"
    
    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("Documnets_chunks_id.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    embedding_model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(1536),
        nullable=False,
    )

    chunk = relationship(
        "document_chunks",
        back_populates="embedding",
    )
    
    
    
     

