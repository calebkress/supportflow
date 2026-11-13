
def sample_ticket():
    return {
        "title": "GPU failure during inference",
        "description": "GPU Xid errors under sustained load.",
        "server_model": "PowerEdge R760xa",
        "error_logs": "NVRM: Xid 79",
    }


def test_create_ticket(client):
    response = client.post("/tickets", json=sample_ticket())

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == sample_ticket()["title"]
    assert data["status"] == "new"
    assert "created_at" in data


def test_list_tickets(client):
    client.post("/tickets", json=sample_ticket())

    response = client.get("/tickets")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_ticket(client):
    created = client.post(
        "/tickets",
        json=sample_ticket(),
    ).json()

    response = client.get(f"/tickets/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_nonexistent_ticket(client):
    response = client.get("/tickets/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"

def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}