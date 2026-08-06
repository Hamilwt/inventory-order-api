# Inventory & Order Management API

A resilient, cloud-native backend API for managing product inventory and processing customer orders, built to guarantee data integrity during high-stakes financial transactions.

![Python](https://img.shields.io/badge/python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema](#database-schema)
- [How Order Processing Works](#how-order-processing-works)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Error Tracking](#error-tracking)
- [License](#license)

## Overview

This project is a backend API designed to mirror the operations of a real e-commerce or warehouse system: it tracks product inventory, accepts customer orders, and — most importantly — never lets stock and order records fall out of sync. Every order either fully succeeds (stock deducted, order recorded) or fully fails (nothing changes), the same way a bank transfer either completes or bounces back in full.

It is built with a modern, production-style Python stack: fully containerized, migration-driven, tested, and monitored with real error telemetry.

## Features

- **Atomic order processing** — stock deduction and order creation happen in a single database transaction; a failure anywhere rolls back everything.
- **Stock-aware conflict handling** — orders that request more stock than is available are rejected with a `409 Conflict`, and nothing is partially applied.
- **Strict request validation** — Pydantic v2 rejects malformed or nonsensical payloads (e.g. negative quantities) before they reach the database layer.
- **Historical price integrity** — each order line item stores the price at the time of purchase, so later price changes never rewrite order history.
- **Auto-generated API docs** — interactive Scalar UI documentation out of the box via FastAPI.
- **Schema migrations** — Alembic tracks and applies every database change.
- **Automated test suite** — Pytest exercises both the happy path and adversarial cases (e.g. ordering more units than are in stock).
- **Live error telemetry** — Sentry captures unhandled exceptions in production with full stack traces.
- **Containerized** — identical behavior on any machine via Docker.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Web framework | FastAPI |
| ASGI server | Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Database | PostgreSQL (hosted on Neon) |
| Testing | Pytest |
| Error tracking | Sentry |
| Containerization | Docker |
| Hosting | Render |

## Database Schema

The schema is normalized and deliberately preserves historical accuracy — the `price_at_time_of_order` column exists so that a price change next year never alters what a customer actually paid in a past order.

```mermaid
erDiagram
    PRODUCTS ||--o{ ORDER_ITEMS : "ordered in"
    ORDERS ||--o{ ORDER_ITEMS : contains

    PRODUCTS {
        int id PK
        string name
        float price
        int stock_quantity
    }

    ORDERS {
        int id PK
        int customer_id
        string status
        datetime created_at
    }

    ORDER_ITEMS {
        int order_id FK
        int product_id FK
        int quantity
        float price_at_time_of_order
    }
```

## How Order Processing Works

The `POST /orders` endpoint is the core of the system. Every submitted order runs through the same gauntlet:

1. **Schema validation** — Pydantic rejects malformed input immediately (e.g. a quantity of `-5` returns `422 Unprocessable Entity`).
2. **Stock verification** — the service layer checks current inventory for every item in the cart.
3. **Atomic transaction** — if stock is sufficient, inventory is deducted and the order is written to the database inside one transaction — never one without the other.
4. **Conflict resolution** — if any item lacks sufficient stock, the entire transaction rolls back and the API returns `409 Conflict`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Check if the API is running successfully |
| `GET` | `/products` | List all products |
| `POST` | `/products` | Create a new product |
| `GET` | `/products/{id}` | Get a single product |
| `POST` | `/orders` | Place an order (atomic stock check + creation) |
| `GET` | `/orders/{id}` | Get a single order with its line items |
| `GET` | `/orders` | List all orders |

Full interactive documentation is available at `/docs` (Scalar UI) once the application is running.

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL database (a free [Neon](https://neon.tech) instance works well)
- Docker (optional, but recommended)

### Local Installation

```bash
git clone https://github.com/Hamilwt/inventory-order-api.git
cd inventory-order-api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SENTRY_DSN=your_sentry_dsn_here
```

### Apply Database Migrations

```bash
alembic upgrade head
```

### Run the App

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API docs.

### Run with Docker

```bash
docker build -t inventory-api .
docker run -p 8000:8000 --env-file .env inventory-api
```

## Running Tests

```bash
pytest -v
```

The suite covers both the happy path (valid orders return `200 OK`) and adversarial cases — e.g. requesting 500 units of a product with only 10 in stock correctly returns a `409 Conflict` without touching the database state.

## Deployment

The application is containerized with Docker and deployed on [Render](https://render.com). The live API and its interactive docs are available at:

- **API Base URL:** [https://inventory-and-order-management-api-k53n.onrender.com](https://inventory-and-order-management-api-k53n.onrender.com)
- **Live Documentation:** [https://inventory-and-order-management-api-k53n.onrender.com/docs](https://inventory-and-order-management-api-k53n.onrender.com/docs)

## Project Structure

```
inventory-order-api/
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   └── database.py
├── alembic/
│   └── versions/
├── tests/
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## Error Tracking

Sentry is integrated into the FastAPI middleware. Any unhandled exception in production is captured with a full stack trace, request context, and environment details, and sent to a live dashboard for debugging — the same way you'd expect an on-call engineer's tooling to work.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.