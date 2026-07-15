# Decision Journal API

A RESTful backend application built with **Flask** that helps users improve their decision-making through structured reflection.

Users can record important decisions, document their reasoning and expectations, and later review the actual outcome to compare expectations with reality.

This project was built as a backend engineering learning project with an emphasis on clean architecture, maintainability, testing, and containerization.

---

# Features

* User registration
* JWT authentication
* Protected endpoints
* Create decisions
* Retrieve decisions
* Update open decisions
* Filter decisions by status
* Review completed decisions
* Immutable decision lifecycle after review
* PostgreSQL database
* Alembic migrations
* Pytest integration tests
* Docker & Docker Compose support

---

# Tech Stack

* Python
* Flask
* PostgreSQL
* SQLAlchemy
* Flask-Migrate
* Flask-JWT-Extended
* Pytest
* Docker
* Docker Compose

---

# Project Structure

```text
decision-journal/

app/
│
├── config/
├── decisions/
├── errors/
├── extensions/
├── models/
├── reviews/
├── users/
└── __init__.py

migrations/
tests/

Dockerfile
docker-compose.yml
requirements.txt
run.py
config.py
README.md
```

---

# Architecture

The project follows a feature-based architecture.

Each feature is organized into its own module containing:

* Routes
* Services
* Validation
* Business Logic

Responsibilities are separated as follows:

* **Routes** → Handle HTTP requests and responses
* **Services** → Business logic and database interaction
* **Models** → Database representation
* **Schemas** → Input validation and normalization

---

# Getting Started

## Clone the Repository

```bash
git clone <repository-url>
cd Decision-Journal-Project
```

---

# Running the Application with Docker

## 1. Build the Docker images

```bash
docker compose build
```

---

## 2. Start the containers

```bash
docker compose up
```

Or run them in the background:

```bash
docker compose up -d
```

---

## 3. Apply Database Migrations

Once the containers are running, open a terminal inside the API container:

```bash
docker compose exec api bash
```

Run the migrations:

```bash
flask db upgrade
```

Exit the container:

```bash
exit
```

---

## 4. Verify the Application

The API will be available at:

```text
http://localhost:5000
```

You can test the ping endpoint using Postman to check if the app is up and running.

Example:

```
GET [http://127.0.0.1:5000/api/v1/users/ping]
```

Expected response:

```json
{
    "ping": "pong"
}
```

---

# Running Tests

Execute the test suite:

```bash
pytest
```

---

# Authentication

Most endpoints require a JWT access token.

## Step 1 — Register a User (does not require a JWT token)

```
POST /api/v1/users/signup
```

Example request body:

```json
{
    "name": "Ali",
    "email": "ali@example.com",
    "password": "password123"
}
```

---

## Step 2 — Login

```
POST /api/v1/users/login
```

Example request body:

```json
{
    "email": "ali@example.com",
    "password": "password123"
}
```

If the credentials are correct, the API returns a response containing a JWT access token.

Example:

```json
{
    "token": "<your_access_token>"
}
```

Copy this token.

---

## Step 3 — Authorise Requests in Postman

For every protected endpoint:

1. Open the request in Postman.
2. Go to the **Authorization** tab.
3. Select **Bearer Token**.
4. Paste the token received from the login endpoint.

Alternatively, you can manually add the header:

```text
Authorization: Bearer <your_access_token>
```

---

# Decision Lifecycle

A decision follows the workflow below:

1. Create a decision.
2. Update the decision while its status is **OPEN**.
3. Review the decision.
4. The review automatically changes the decision status to **REVIEWED**.
5. Reviewed decisions become immutable, while the review itself can still be updated.

---

# API Endpoints

## Users

| Method | Endpoint               |
| ------ | ---------------------- |
| POST   | `/api/v1/users/signup` |
| POST   | `/api/v1/users/login`  |
| GET    | `/api/v1/users/me`     |

---

## Decisions

| Method | Endpoint                            |
| ------ | ----------------------------------- |
| POST   | `/api/v1/decisions`                 |
| GET    | `/api/v1/decisions`                 |
| GET    | `/api/v1/decisions/<id>`            |
| PATCH  | `/api/v1/decisions/<id>`            |
| GET    | `/api/v1/decisions/status/<status>` |

---

## Reviews

| Method | Endpoint          |
| ------ | ----------------- |
| POST   | `/api/v1/reviews` |

---

# License

This project was created for educational purposes to practice backend engineering principles, clean architecture, and production-oriented API development.
