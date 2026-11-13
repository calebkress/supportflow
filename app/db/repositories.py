
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.models.ticket_schema import TicketCreate
from app.models.triage import TicketTriage
from app.models.triage_schema import TriageResult


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, ticket: TicketCreate) -> Ticket:
        db_ticket = Ticket(**ticket.model_dump())

        self.db.add(db_ticket)
        self.db.commit()
        self.db.refresh(db_ticket)

        return db_ticket

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        return self.db.get(Ticket, ticket_id)

    def get_all(self) -> list[Ticket]:
        statement = select(Ticket).order_by(
            Ticket.created_at.desc()
        )

        return list(self.db.scalars(statement).all())
    
    def save_triage(
        self,
        ticket: Ticket,
        result: TriageResult,
    ) -> TicketTriage:
        triage = TicketTriage(
            ticket_id=ticket.id,
            **result.model_dump(),
        )

        self.db.add(triage)
        ticket.status = "triaged"

        self.db.commit()
        self.db.refresh(triage)

        return triage

    def get_triage_history(
        self,
        ticket_id: int,
    ) -> list[TicketTriage]:
        statement = (
            select(TicketTriage)
            .where(TicketTriage.ticket_id == ticket_id)
            .order_by(TicketTriage.created_at.desc())
        )

        return list(self.db.scalars(statement).all())

