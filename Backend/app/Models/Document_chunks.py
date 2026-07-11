from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy import String,ForeignKey,Text,Integer

from Backend.app.Models.base_model import BaseModel

class document_chunks(BaseModel):
    
    __tablename__ = "Document_chunks_table"
    
    Documnets_chunks_id : Mapped[int] = mapped_column(
        ForeignKey("documents.id"),# documents.id the first part is table u want to use the primary key.id in
        nullable=False,
        index=True,
    )
    
    chunk_index : Mapped[int] = mapped_column(
        index=True,
        nullable=False,
    )
    
    content : Mapped[str] = mapped_column(
        Text,
        nullable=False,
        index=True,
    )
    
    token_count : Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )
    
    document = relationship(
    "Document",# class name of primary key in
    back_populates="chunks",# the ralationship connection name in the document class
    )
    
    