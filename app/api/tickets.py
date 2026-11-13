
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from openai import OpenAIError

from app.services.triage import TriageService
from app.models.triage_schema import TriageResult

from app.db.database import get_db
from app.db.repositories import TicketRepository

from app.models.ticket_schema import (
    TicketCreate,
    TicketResponse,
)


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)


def get_repository(db: Session = Depends(get_db)):
    return TicketRepository(db)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=201,
)
def create_ticket(
    ticket: TicketCreate,
    repo: TicketRepository = Depends(get_repository),
):
    return repo.create(ticket)


@router.get("", response_model=list[TicketResponse])
def list_tickets(
    repo: TicketRepository = Depends(get_repository),
):
    return repo.get_all()


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    repo: TicketRepository = Depends(get_repository),
):
    ticket = repo.get_by_id(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket

def get_triage_service():
    return TriageService()


@router.post(
    "/{ticket_id}/triage",
    response_model=TriageResult,
)
def triage_ticket(
    ticket_id: int,
    repo: TicketRepository = Depends(get_repository),
    service: TriageService = Depends(get_triage_service),
):
    ticket = repo.get_by_id(ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    try:
        result = service.classify(ticket)
    except (OpenAIError, ValueError):
        raise HTTPException(
            status_code=502,
            detail="Ticket classification failed",
        )

    repo.save_triage(ticket, result)

    return result
