# SupportFlow

**AI-Assisted Infrastructure Support Automation**

SupportFlow is a Python-based technical support automation project designed to explore how structured AI workflows can improve the efficiency, consistency, and reliability of enterprise infrastructure support.

The system combines a REST API, persistent ticket management, and a modular service architecture with the goal of automating repetitive support operations while preserving human oversight for potentially disruptive actions.

> **Project Status:** Early development — core ticket management API implemented; AI triage and diagnostic automation in progress.

## Overview

Enterprise infrastructure support often involves repetitive processes: reviewing incoming tickets, identifying likely causes, consulting troubleshooting documentation, and determining whether an issue can be resolved automatically or requires escalation.

SupportFlow is designed around a simple principle:

**AI interprets technical problems. Deterministic application logic governs operational actions.**

The goal is not to replace support engineers, but to reduce repetitive triage work and provide consistent, auditable troubleshooting recommendations.

## Architecture

SupportFlow uses a modular Python backend built with FastAPI and SQLAlchemy.

```text
                  ┌─────────────────────┐
                  │    REST API Client  │
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │    FastAPI Layer    │
                  │  Request Validation │
                  │   HTTP Endpoints    │
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │   Repository Layer  │
                  │  Database Operations│
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │ SQLAlchemy + SQLite │
                  │  Persistent Storage │
                  └─────────────────────┘

          Planned AI Automation Components
                             │
                  ┌──────────▼──────────┐
                  │  AI Triage Service  │
                  │ Structured Outputs  │
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │  Runbook Retrieval  │
                  │  Diagnostic Matching│
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │    Policy Engine    │
                  │  Approval & Safety  │
                  └──────────┬──────────┘
                             │
                  ┌──────────▼──────────┐
                  │ Workflow Executor   │
                  │ Simulated Diagnostics│
                  └─────────────────────┘
```

The application is intentionally designed as a modular monolith. This keeps deployment and development straightforward while maintaining clear boundaries between HTTP handling, persistence, AI reasoning, and workflow execution.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| API Framework | FastAPI |
| Data Validation | Pydantic |
| ORM | SQLAlchemy 2.x |
| Database | SQLite |
| Schema Migrations | Alembic |
| Testing | pytest, pytest-cov |
| AI Integration (Planned) | OpenAI API |
| Dashboard (Planned) | Streamlit |

## Current Features

### Ticket Management API

- Create infrastructure support tickets with validated request payloads.
- Retrieve individual tickets by ID.
- List existing tickets.
- Persist ticket records using SQLAlchemy and SQLite.
- Return structured JSON responses with appropriate HTTP status codes.

### Database Management

- Version-controlled database schema migrations using Alembic.
- Repository abstraction separating persistence logic from API endpoints.
- Environment-based configuration.

### Automated Testing

- API integration tests using FastAPI's TestClient and pytest.
- Isolated in-memory SQLite databases for testing.
- Tests covering ticket creation, retrieval, listing, and missing-resource handling.
- 95% statement coverage at the completion of the initial backend milestone.

## API Reference

FastAPI automatically generates interactive API documentation at `/docs`.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| POST | `/tickets` | Create a support ticket |
| GET | `/tickets` | Retrieve all tickets |
| GET | `/tickets/{ticket_id}` | Retrieve a ticket by ID |

### Example: Create a Ticket

**Request**

```http
POST /tickets
Content-Type: application/json
```

```json
{
  "title": "GPU failure during inference",
  "description": "Server reports intermittent GPU errors under sustained inference workloads.",
  "server_model": "PowerEdge R760xa",
  "error_logs": "NVRM: Xid 79, GPU has fallen off the bus"
}
```

**Response — HTTP 201**

```json
{
  "id": 1,
  "title": "GPU failure during inference",
  "description": "Server reports intermittent GPU errors under sustained inference workloads.",
  "server_model": "PowerEdge R760xa",
  "error_logs": "NVRM: Xid 79, GPU has fallen off the bus",
  "status": "new",
  "created_at": "2026-11-13T22:00:00"
}
```

## Getting Started

### Prerequisites

- Python 3.12+
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/calebkress/supportflow.git
cd supportflow
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Configuration

Copy the example environment configuration:

```bash
cp .env.example .env
```

The default configuration uses a local SQLite database.

An OpenAI API key is not required for the currently implemented ticket management endpoints.

### Database Setup

Apply the database migrations:

```bash
alembic upgrade head
```

### Run the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Interactive documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Testing

Run the test suite:

```bash
python -m pytest -v
```

Generate a coverage report:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Tests use isolated SQLite databases to prevent modification of development data.

## Development Roadmap

### Phase 1 — Backend Foundation

- [x] FastAPI application scaffolding
- [x] Environment-based configuration
- [x] SQLAlchemy models and SQLite persistence
- [x] Alembic database migrations
- [x] Ticket CRUD endpoints (create and read)
- [x] Repository abstraction
- [x] Automated API tests

### Phase 2 — AI-Assisted Triage

- [ ] Structured ticket classification using an LLM
- [ ] Severity and category assignment
- [ ] Persisted classification history
- [ ] Error handling and fallback behavior
- [ ] Automated evaluation against synthetic support tickets

### Phase 3 — Knowledge Retrieval

- [ ] Structured troubleshooting runbooks
- [ ] Context-aware runbook matching
- [ ] Diagnostic recommendations
- [ ] Retrieval quality evaluation

### Phase 4 — Workflow Automation

- [ ] Deterministic policy engine
- [ ] Action allowlisting
- [ ] Human approval for sensitive operations
- [ ] Simulated diagnostic execution
- [ ] Audit logging

### Phase 5 — Dashboard

- [ ] Streamlit support ticket interface
- [ ] Ticket classification and workflow visibility
- [ ] Diagnostic recommendations
- [ ] Human approval controls

## Design Principles

**Separation of concerns:** API routes handle HTTP interactions, repositories handle persistence, and services encapsulate application logic.

**Human oversight:** AI-generated recommendations do not independently authorize infrastructure changes.

**Testability:** External dependencies are designed to be replaceable with test doubles, enabling deterministic automated testing.

**Incremental development:** Each subsystem is implemented and validated independently before introducing additional complexity.

**Operational transparency:** Future workflow execution will include explicit status tracking and auditable action histories.

## Project Scope

SupportFlow is an independent educational and portfolio project. It uses synthetic infrastructure support scenarios and is not affiliated with, endorsed by, or integrated into any infrastructure vendor.

The project is not intended to execute operations against production infrastructure.

## License
g
This project is licensed under the MIT License. See the LICENSE file for details.

---

*Built to explore practical applications of AI-assisted workflow automation in enterprise technical support.*