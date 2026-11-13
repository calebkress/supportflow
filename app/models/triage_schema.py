
from enum import Enum

from pydantic import BaseModel, Field


class TicketCategory(str, Enum):
    GPU = "gpu"
    NETWORK = "network"
    STORAGE = "storage"
    FIRMWARE = "firmware"
    THERMAL = "thermal"
    OTHER = "other"


class TriageResult(BaseModel):
    category: TicketCategory
    severity: int = Field(ge=1, le=4)
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    recommended_action: str
    requires_escalation: bool
