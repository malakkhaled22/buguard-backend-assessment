# Asset Management System (DarkAtlas Module)

A backend system for managing and tracking internet-facing assets as part of an Attack Surface Monitoring (ASM) platform.

This project was developed as an internship technical assessment for Backend Engineering.

## Tech Stack

* Python 3.11
* FastAPI
* PostgreSQL
* SQLAlchemy
* Docker
* Pytest

## Features

* Asset CRUD Operations
* Bulk Import
* Deduplication
* Lifecycle Tracking
* Asset Relationships
* Filtering
* Pagination
* Tag Management
* API Key Authentication
* Automated Tests

## Setup

### Clone Repository

```bash
git clone <repo-url>
cd asset-management
```

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/assets
API_KEY=your-buguard-strong-key
GEMINI_API_KEY=your-gemini-api-key //for (langChain) bonus
```

## Run with Docker

```bash
docker compose up --build
```

## API Authentication

Protected endpoints require:

X-API-Key: your-buguard-strong-key

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

## Running Tests

```bash
pytest
```

## Bonus - LangChain AI Risk Assessment

A LangChain-powered endpoint was added to analyze assets and generate a security risk assessment using Google Gemini.

Endpoint:

POST /ai/risk/{asset_id}

Returns:

- Risk Level
- AI-generated explanation

## Design Decisions

* SQLAlchemy ORM was used for database access.
* Asset deduplication is based on `(type, value)` uniqueness.
* JSON metadata allows flexible asset-specific fields.
* API Key authentication protects write operations.
* Relationships are stored separately to support graph-like asset connections.

## Assumptions

* Assets are uniquely identified by their type and value.
* Re-importing an existing asset updates `last_seen`.
* Metadata is merged during import.
* Tags are merged without duplication.

## Future Improvements

* RBAC Authentication
* Multi-tenancy
* Graph Visualization
* Risk Scoring
* Async Database Layer