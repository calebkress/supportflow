
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.ticket import Ticket
from app.models.ticket_schema import (
    TicketCreate,
    TicketResponse,
)


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
)


@router.post(
    "",
    response_model=TicketResponse,
    status_code=201,
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
):
    db_ticket = Ticket(**ticket.model_dump())

    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)

    return db_ticket


@router.get("", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    statement = select(Ticket).order_by(
        Ticket.created_at.desc()
    )

    return db.scalars(statement).all()


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket
