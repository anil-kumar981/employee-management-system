# 🚀 Employee Management System

A production-grade, highly structured **Employee Management System** built with **Python 3**, **Flask**, and **SQLAlchemy 2.0 ORM** following a strict **Layered Architecture** design. 

This project incorporates clean coding practices, **Dependency Injection (DI)**, **100% Native Asynchronous Database Queries (`asyncpg` + `AsyncSession`)**, **Pydantic v2 Request Validation**, and **Centralized Global Exception Mapping**.

---

## 🌟 Architectural Features

### 1. Decoupled Layered Architecture (SOLID)
* **Controller Layer (Router)**: Handled by standard Flask blueprints and view routers. It is only responsible for receiving HTTP requests, validating request bodies, and returning standard JSON payloads.
* **Service Layer (Business Logic)**: Houses business rules (uniqueness validations, partial update merging, presence checks) and validation logic, fully decoupled using abstract interfaces.
* **Repository Layer (Data Access)**: Concrete database transactions utilizing **SQLAlchemy 2.0 ORM**. Handles CRUD operations natively and is isolated from the service layer via interfaces.
* **Dependency Injection Container**: Dynamic instantiation inside dependency providers, injecting repositories directly into services.

### 2. 100% Native Asynchronous Non-Blocking Database Queries
* All database queries are natively asynchronous utilizing **`asyncpg`** (the fastest async PostgreSQL driver for Python) and SQLAlchemy's **`AsyncSession`**.
* Eliminates thread-blocking constraints, unlocking high-concurrency scaling.

### 3. Pydantic-based Request Validation & Global Error Handling
* Incoming JSON payloads are validated at the route boundary using a custom `@validate_request` decorator and Pydantic schemas.
* Global exceptions are caught by centralized middleware, mapping database conflicts, entity absences, or validation failures into clean API responses.

---

## 📂 Project Directory Structure

```text
employee-management-system/
├── app/
│   ├── controllers/             # Presentational Controllers (Routers)
│   │   └── employee_controller.py
│   ├── core/                    # System cores (app factory, DB binds, exceptions)
│   │   ├── config.py
│   │   └── database.py          # Native Async Engine & SessionMaker
│   ├── decorators/              # Custom decorators (FastAPI-style validation decorator)
│   │   └── decorator.py
│   ├── dependencies/            # Dependency Injection Registry (DI Container)
│   │   └── employee_dependencies.py
│   ├── model/                   # SQLAlchemy Database Models
│   │   └── employee.py
│   ├── repositories/            # Data Access Layer (Abstract & Concrete)
│   │   ├── interface/
│   │   │   ├── ibase_repository.py
│   │   │   └── iemployee_repository.py
│   │   ├── base_repository.py   # Generic Concrete BaseRepo[T]
│   │   └── employee_repository.py
│   ├── schema/                  # Validation Schemas (Pydantic Models)
│   │   └── employee.py
│   ├── services/                # Business Logic Layer (Abstract & Concrete)
│   │   ├── interface/
│   │   │   └── iemployee_service.py
│   │   └── employee_service.py
│   ├── shared/                  # Common responses and exceptions
│   │   ├── api_response/
│   │   │   └── response_factory.py
│   │   └── exceptions.py
│   └── test/                    # Full-layered Pytest Suite
│       ├── test_controller.py
│       ├── test_repository.py
│       └── test_service.py
├── migrations/                  # Alembic DB Migration history
├── .env                         # Server environment parameters
├── alembic.ini                  # Alembic setup configuration
├── main.py                      # WSGI Entrypoint (standard server)
├── asgi.py                      # ASGI Entrypoint (wrapped event-loop server)
├── Dockerfile                   # Production Docker configuration
└── requirements.txt             # Installed dependencies list
```

---

## 🚀 Getting Started (Local Setup)

### 1. Clone the Repository
Clone the codebase to your local machine using git:
```bash
git clone https://github.com/anil-kumar981/employee-management-system.git
cd employee-management-system
```

### 2. Create & Activate Virtual Environment
Set up a clean virtual environment to isolate project dependencies:

* **On Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
* **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
* **On macOS / Linux / Git Bash:**
  ```bash
  python3 -m venv venv
  source venv/Scripts/activate
  ```

### 3. Install Dependencies
Install all required libraries, engines, and ORM components:
```bash
pip install -r requirements.txt
```

### 4. Database Setup & Configurations
1. Ensure a PostgreSQL database server is running locally on port `5432`.
2. Create an empty database named `Employee_management_System`.
3. Create a `.env` file in the root folder (or update the existing one) with your credentials:
   ```env
   FLASK_ENV=development
   PORT=5000
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/Employee_management_System
   ```

### 5. Running Alembic DB Migrations
The database schema is fully managed via Alembic. Run these commands to apply or create migrations:

* **Apply existing migrations to the database:**
  ```bash
  alembic upgrade head
  ```
* **Create a new migration after updating models:**
  ```bash
  alembic revision --autogenerate -m "migration_description"
  ```
* **How to revert/remove a wrong migration:**
  * **Case 1: If migration is NOT yet applied to the database:**
    Simply delete the generated python script file from the `migrations/versions/` directory.
  * **Case 2: If migration is ALREADY applied to the database:**
    1. Downgrade the database schema by one step:
       ```bash
       alembic downgrade -1
       ```
    2. Delete the incorrect migration python script file from the `migrations/versions/` directory.

> [!NOTE]
> The application will also automatically check and apply any pending migrations silently during server startup!

---

## 🏃 Running the Application

You can execute this project in two distinct modes depending on your target performance needs:

### Option A: Standard Web Server (`python main.py`)
* **Command:** 
  ```bash
  python main.py
  ```
* **Purpose:** Runs the standard Flask development server in WSGI mode.
* **How it works:** Handles incoming requests in synchronous thread pools. Ideal for simple local debugging, quick route testing, and standard development.

### Option B: High-Performance Async Server (`python asgi.py`)
* **Command:** 
  ```bash
  python asgi.py
  ```
* **Purpose:** Runs a fully-adapted ASGI application served via `uvicorn`.
* **How it works:** Wraps Flask inside `WsgiToAsgi` from the `asgiref` package, allowing it to hook into an event loop. This enables natively non-blocking async network sockets and leverages uvicorn's event loop to achieve high connection scaling.

---

## 🐳 Running with Docker

### 1. Development Mode (Includes DB Container)
Builds the app container, spins up an isolated PostgreSQL container, and links them automatically:
```bash
docker compose -f docker-compose.dev.yml up --build
```
* **URL:** `http://localhost:5000`
* **Interactive API Docs:** `http://localhost:5000/swagger-ui`

### 2. Production Mode (Standalone App)
Runs the standalone optimized application container, pointing to the external database host set in `.env`:
```bash
docker compose -f docker-compose.prod.yml up --build
```

---

## 📑 API Endpoints & Contract Formats

All API endpoints return standard, clean JSON payloads.

| Method | Path | Description | Request Format | Response Format (Success 200/201) |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/employees/` | Add a new employee record | `{ "name": "John Doe", "email": "john@example.com", "department": "HR", "date_joined": "2026-06-01" }` | `{ "success": true, "message": "Employee...created.", "data": { "id": 1, "name": "John Doe", ... } }` |
| **GET** | `/employees/` | Fetch list of all employees | *None* | `{ "success": true, "message": "Successfully retrieved 1 record.", "data": [...] }` |
| **GET** | `/employees/{id}` | Get details of a single employee | *None* | `{ "success": true, "message": "...", "data": { "id": 1, "name": "John Doe", ... } }` |
| **PUT** | `/employees/{id}` | Modify details of an employee | `{ "department": "Engineering" }` *(Partial update supported)* | `{ "success": true, "message": "...", "data": { "id": 1, "department": "Engineering", ... } }` |
| **DELETE**| `/employees/{id}` | Remove employee from the database | *None* | `{ "success": true, "message": "Employee with ID 1 was deleted.", "data": null }` |

---

## 🧪 Running Unit Tests
We provide a comprehensive layered testing suite using mock objects for database interfaces:
```bash
pytest app/test/ -v
```
