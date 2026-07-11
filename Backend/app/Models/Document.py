from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Backend.app.Models.Enum import Document_Status
from sqlalchemy import Enum

from Backend.app.Models.base_model import BaseModel


class Document(BaseModel):
    """
    Stores uploaded document metadata.

    The actual file is stored in object storage
    (AWS S3, Azure Blob, MinIO, Local Storage).

    This table stores only metadata.
    """

    __tablename__ = "documents"

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True,
    )

    file_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    processing_status: Mapped[Document_Status] = mapped_column(
        Enum(Document_Status),
        default=Document_Status.UPLOADED,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    # Relationship with User
    user = relationship(
        "User",
        back_populates="documents",
    )

    # Relationship with Document Chunks
    chunks = relationship(
    "document_chunks",
    back_populates="document",
    cascade="all, delete-orphan",
)