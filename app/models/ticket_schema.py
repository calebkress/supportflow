
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TicketStatus(str, Enum):
    NEW = "new"
    TRIAGED = "triaged"
    NEEDS_REVIEW = "needs_review"
    RESOLVED = "resolved"


class TicketCreate(BaseModel):
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10)
    server_model: str | None = None
    error_logs: str | None = None


class TicketResponse(TicketCreate):
    id: int
    status: TicketStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
