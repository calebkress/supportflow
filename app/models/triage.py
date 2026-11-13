
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TicketTriage(Base):
    __tablename__ = "ticket_triages"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    severity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    confidence: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    summary: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    recommended_action: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    requires_escalation: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
