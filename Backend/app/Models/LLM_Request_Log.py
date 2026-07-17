from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Backend.app.Models.base_model import BaseModel


class LLMRequestLog(BaseModel):

    __tablename__ = "llm_request_logs"

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    prompt_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    completion_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    total_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    latency_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    estimated_cost: Mapped[float] = mapped_column(
        Numeric(10, 4),
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="llm_requests",
    )