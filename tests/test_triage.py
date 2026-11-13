
from app.api.tickets import get_triage_service
from app.main import app
from app.models.triage_schema import (
    TicketCategory,
    TriageResult,
)


class FakeTriageService:
    def classify(self, ticket):
        return TriageResult(
            category=TicketCategory.GPU,
            severity=2,
            confidence=0.95,
            summary="GPU connectivity failure detected.",
            recommended_action="Inspect GPU logs.",
            requires_escalation=True,
        )


def test_triage_ticket(client):
    app.dependency_overrides[get_triage_service] = (
        lambda: FakeTriageService()
    )

    try:
        created = client.post(
            "/tickets",
            json={
                "title": "GPU failure",
                "description": "GPU disappeared during inference.",
            },
        ).json()

        response = client.post(
            f"/tickets/{created['id']}/triage"
        )

        assert response.status_code == 200
        assert response.json()["category"] == "gpu"
        assert response.json()["severity"] == 2

        ticket = client.get(
            f"/tickets/{created['id']}"
        ).json()

        assert ticket["status"] == "triaged"

    finally:
        app.dependency_overrides.pop(
            get_triage_service, None
        )
