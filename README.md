# Employee Management System

A production-grade, highly structured **Employee Management System** built with **Python 3**, **Flask**, and **SQLAlchemy 2.0 ORM** following a strict **Layered Architecture** design. 

This project incorporates the solid, decoupled concepts of **Dependency Injection (DI)**, **Dependency Inversion (SOLID)**, **Asynchronous Thread Execution (`asyncio.to_thread`)**, **Dual-Schema Validation (Pydantic + Marshmallow)**, and **Centralized Global Exception Mapping**.

---

## 🌟 Architectural Features

### 1. Decoupled Layered Architecture (SOLID)
- **Controller Layer (Router)**: Handled by `flask-smorest` class-based view routers. Only responsible for receiving HTTP requests, binding Swagger parameters, and returning standard JSON payloads. It has zero awareness of database schemas or database drivers.
- **Service Layer (Business Logic)**: Houses business rules (uniqueness validations, partial update merging, resource presence checks) and orchestrates payloads. Runs deep structural assertions via **Pydantic v2**.
- **Repository Layer (Data Access)**: Concrete database transactions utilizing **SQLAlchemy 2.0 ORM** mapping. Decoupled using an abstract base class (`abc.ABC`).
- **Dependency Injection Container**: Dynamic instantiation inside `app/dependencies/container.py` injected into services and controllers, ensuring components are completely loose and testable.

### 2. High-Performance Non-Blocking Database Queries
- Although utilizing the synchronous `psycopg2` / `sqlite3` drivers, the **Repository Layer** methods are defined as `async def`.
- Inside the repository, blocking database queries (commits, loads) are dispatched to separate background threadpools via **`asyncio.to_thread`**. This prevents blocking the main Flask event loop, drastically improving server throughput.

### 3. Dual-Schema Validation Pattern
- **Pydantic v2 Schemas** (`app/schema/employee.py`): Performs core structural logic validation (RFC-compliant email, whitespace trimming, date formatting) in the **Service Layer** to preserve database integrity.
- **Marshmallow Schemas** (`app/schema/marshmallow_schemas.py`): Registered with `flask-smorest` views to **auto-generate interactive OpenAPI Swagger UI specs**.

### 4. Standardized Dynamic Response Factory & Centralized Handlers
- Centralized `ApiResponseFactory` formats every successful response and error into a uniform JSON structure.
- Messages are fully dynamic (e.g., `"Employee 'John Doe' was successfully created with ID 5"` instead of `"Success"`).
- Global exception handlers catch semantic custom errors (`ValidationError`, `EntityNotFoundException`, `ConflictException`) and map them to standard HTTP status codes.

---

## 📂 Project Directory Structure

```text
employee-management-system/
├── app/
│   ├── controllers/             # Presentational Controllers (Routers)
│   │   └── employee_controller.py
│   ├── core/                    # System cores (app factory, DB binds, exceptions)
│   │   ├── config.py
│   │   ├── database.py
│   │   └── error_handlers.py
│   ├── dependencies/            # Dependency Injection Registry (DI Container)
│   │   └── container.py
│   ├── model/                   # SQLAlchemy Database Models
│   │   └── employee.py
│   ├── repositories/            # Data Access Layer (Abstract & Concrete)
│   │   ├── base_repository.py
│   │   └── employee_repository.py
│   ├── schema/                  # Validation Schemas (Pydantic & Marshmallow)
│   │   ├── employee.py
│   │   └── marshmallow_schemas.py
│   ├── services/                # Business Logic Layer (Abstract & Concrete)
│   │   ├── base_service.py
│   │   └── employee_service.py
│   ├── shared/                  # Common responses and exceptions
│   │   ├── exceptions.py
│   │   └── response_factory.py
│   └── test/                    # Full-layered Pytest Suite
│       ├── test_controller.py
│       ├── test_repository.py
│       └── test_service.py
├── migrations/                  # Alembic DB Migration history
├── .env                         # Server environment parameters
├── alembic.ini                  # Alembic setup configuration
├── main.py                      # Server runner entrypoint
└── requirements.txt             # Installed dependencies list
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+** (System is tested on Python 3.14)
- **Virtual Environment**

### 2. Environment Configuration
The system uses `.env` in the root directory. Rename/configure it with your parameters:
```env
# Server configuration
FLASK_ENV=development
PORT=5000

# Database Configuration
# Fallback SQLite for instant zero-config startup:
DATABASE_URL=sqlite:///employee_management.db

# To use local PostgreSQL local instance:
# DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
```

### 3. Setup Virtual Environment & Run Setup
```powershell
# 1. Activate your virtual environment
.\venv\Scripts\activate

# 2. Run the main server (DB schemas will auto-initialize instantly!)
python main.py
```

---

## 📑 Interactive API Documentation (Swagger)

Once the server is running, visit **`http://localhost:5000/swagger-ui`** to access the premium interactive API documentation interface. You can test endpoints directly inside your browser!

---

## 🧪 Running the Pytest Suite
We provide a 100% mocked layered testing suite verifying the Controller, Service, and Repository layers independently.

```powershell
# Run the complete test suite:
pytest app/test/ -v
```

---

## 🔌 API Reference Specifications

All endpoints return a uniform wrapped JSON structure:
```json
{
  "success": true,
  "message": "Dynamic descriptive operation outcome message.",
  "data": { ... }
}
```

| Method | Endpoint | Description | Expected Request Body | Status Code |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/employees/` | Add a new employee. | See Create Schema | `201 Created` |
| **GET** | `/employees/` | Retrieve a list of all employees. | None | `200 OK` |
| **GET** | `/employees/{id}` | Retrieve details of a specific employee. | None | `200 OK` |
| **PUT** | `/employees/{id}` | Update an existing employee's details. | See Update Schema | `200 OK` |
| **DELETE** | `/employees/{id}` | Remove an employee from the system. | None | `200 OK` |

### Expected Schema Formats

#### 1. Employee Create Schema (POST)
```json
{
  "name": "Alice Smith",
  "email": "alice.smith@example.com",
  "department": "Engineering",
  "date_joined": "2026-06-02"
}
```

#### 2. Employee Update Schema (PUT)
*All fields are optional for partial updates:*
```json
{
  "name": "Alice Jenkins",
  "department": "Infrastructure"
}
```

#### 3. Error Response Format (e.g., 400 Bad Request)
```json
{
  "success": false,
  "message": "Validation failed: Email must be a valid email address.",
  "errors": {
    "email": "value is not a valid email address"
  }
}
```
