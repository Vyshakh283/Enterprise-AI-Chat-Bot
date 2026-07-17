from sqlalchemy import ForeignKey, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from Backend.app.Models.base_model import BaseModel


class SQLQueryLog(BaseModel):

    __tablename__ = "sql_query_logs"

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
    )

    generated_sql: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    execution_success: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    conversation = relationship(
        "Conversation",
        back_populates="sql_queries",
    )