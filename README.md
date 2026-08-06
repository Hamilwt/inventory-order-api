# Inventory and Order Management API

A RESTful backend service for managing product inventory and processing e-commerce orders. Built with FastAPI and PostgreSQL, this project implements atomic database transactions to ensure data consistency during order fulfillment, schema migrations via Alembic, and integrated OpenAPI documentation.

## Architecture

* **Web Framework:** FastAPI (Python 3.13)
* **Database:** PostgreSQL (Neon Serverless)
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **API Client:** Scalar

## Setup

### Local Development

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Hamilwt/inventory-order-api.git](https://github.com/Hamilwt/inventory-order-api.git)
   cd inventory-order-api
   ```

2. **Configure environment variables**
   Create a `.env` file in the project root containing your database connection string:
   ```env
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

3. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

5. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t inventory-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 --env-file .env inventory-api
   ```

## API Documentation

When the application is running, the interactive OpenAPI client (Scalar) is served at:
`http://localhost:8000/docs`
