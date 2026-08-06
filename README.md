# 📦 Inventory & Order Management API

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker)

A professional, high-performance RESTful API built to manage e-commerce inventory and process secure orders. This backend architecture focuses on data integrity, utilizing robust database transactions to prevent race conditions and overselling.

## 🚀 Key Features

*   **All-or-Nothing Transactions:** Secure order processing logic that strictly verifies stock limits and locks in pricing before committing to the database. If an inventory check fails, the entire SQL transaction rolls back instantly.
*   **Full CRUD Architecture:** Complete lifecycle management for both Products and Orders.
*   **Modern Interactive Documentation:** Integrated with Scalar to provide a sleek, dark-mode API client directly in the browser for seamless testing.
*   **Cloud Database Integration:** Connected to a remote PostgreSQL database (Neon) mapped via SQLAlchemy ORM and tracked using Alembic migrations.
*   **Containerized (Docker Ready):** Fully packaged with a `Dockerfile` for standardized, "works-on-my-machine" guaranteed deployments.

## 🛠️ Tech Stack

*   **Framework:** FastAPI
*   **Language:** Python 3.13
*   **Database:** PostgreSQL (Neon Serverless)
*   **ORM:** SQLAlchemy
*   **Migrations:** Alembic
*   **Documentation UI:** Scalar

## 💻 Quick Start (Local Development)

### 1. Clone the repository
```bash
git clone [https://github.com/Hamilwt/inventory-order-api.git](https://github.com/Hamilwt/inventory-order-api.git)
cd inventory-order-api

2. Set up the environment

Create a .env file in the root directory and add your database connection URL:
Code snippet

DATABASE_URL=postgresql://user:password@host/dbname

3. Run with Docker (Recommended)
Bash

docker build -t inventory-api .
docker run -p 8000:8000 inventory-api

4. Access the API

Once running, open your browser and navigate to the interactive dashboard:

    Scalar UI / API Client: http://localhost:8000/docs


### Step 3: Commit and Push the Branch
Save the `README.md` file (`Ctrl + S`), then run these commands in your terminal to push your new branch to GitHub:
```bash
git add README.md
git commit -m "docs: create professional readme with architecture and setup instructions"
git push -u origin docs/add-readme  