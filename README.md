# Employee Management System

A production-grade, highly structured **Employee Management System** built with **Python 3**, **Flask**, and **SQLAlchemy 2.0 ORM** following a strict **Layered Architecture** design. 

This project incorporates the solid, decoupled concepts of **Dependency Injection (DI)**, **Dependency Inversion (SOLID)**, **100% Native Asynchronous Database Queries (`asyncpg` + `AsyncSession`)**, **Pydantic v2 Request Validation**, and **Centralized Global Exception Mapping**.

---

## 🌟 Architectural Features

### 1. Decoupled Layered Architecture (SOLID)
- **Controller Layer (Router)**: Handled by standard Flask blueprints and view routers. Only responsible for receiving HTTP requests, validating request bodies against Pydantic models, and returning standard JSON payloads.
- **Service Layer (Business Logic)**: Houses business rules (uniqueness validations, partial update merging, resource presence checks) and orchestrates payloads, depending on abstract interfaces: [iemployee_service.py](file:///e:/employee-management-system/app/services/interface/iemployee_service.py).
- **Repository Layer (Data Access)**: Concrete database transactions utilizing **SQLAlchemy 2.0 ORM** mapping. Decoupled using an abstract base class hierarchy: [ibase_repository.py](file:///e:/employee-management-system/app/repositories/interface/ibase_repository.py) and [iemployee_repository.py](file:///e:/employee-management-system/app/repositories/interface/iemployee_repository.py).
- **Dependency Injection Container**: Dynamic instantiation inside [employee_dependencies.py](file:///e:/employee-management-system/app/dependencies/employee_dependencies.py) injected into services and repositories.

### 2. 100% Native Asynchronous Non-Blocking Database Queries (Fast!)
- All database queries are **100% natively asynchronous** utilizing **`asyncpg`** (the fastest asynchronous PostgreSQL driver for Python) and SQLAlchemy's **`AsyncSession`**.
- Database queries run directly over non-blocking TCP sockets, exactly like **Node.js/NestJS**, completely eliminating the need for blocking synchronous drivers and background worker threads!

### 3. FastAPI-Style Pydantic Validator Decorator
- Incoming JSON payloads are validated at the route boundary using the custom `@validate_request(Schema)` decorator. 
- Fully-validated Pydantic models are injected directly as arguments (`body`) into the route function signatures.

### 4. Dynamic OpenAPI Swagger UI specs
- Dynamically generates the OpenAPI 3.0.3 specification by extracting JSON schemas directly from your Pydantic schemas using `.model_json_schema()`, serving an interactive Swagger interface at `/swagger-ui`.

---

## 📂 Project Directory Structure

```text
employee-management-system/
├── app/
│   ├── controllers/             # Presentational Controllers (Routers)
│   │   └── employee_controller.py
│   ├── core/                    # System cores (app factory, DB binds, exceptions)
│   │   ├── config.py
│   │   ├── database.py          # Native Async Engine & SessionMaker
│   │   ├── error_handlers.py
│   │   └── swagger.py           # Dynamic OpenAPI Specification Generator
│   ├── decorators/              # Custom decorators (FastAPI-style validator)
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
│       ├── test_repository.py   # Mocks AsyncSession context managers
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
- **PostgreSQL 18** database running locally.
- **pgAdmin** or standard shell.

### 2. Environment Configuration
The system uses `.env` in the root directory. Configure it with your PostgreSQL parameters:
```env
# Server configuration
FLASK_ENV=development
PORT=5000

# Database Configuration
# Local PostgreSQL 18 connection with native asyncpg driver
DATABASE_URL=postgresql+asyncpg://postgres:@Admin123@localhost:5432/Employee_management_System
```

### 3. Database Schema Setup
Ensure your local PostgreSQL server is running and create a database named `Employee_management_System`.

### 4. Setup Virtual Environment & Run Setup
```powershell
# 1. Activate your virtual environment
source venv/Scripts/activate # Git Bash
# or .\venv\Scripts\activate # PowerShell

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

## 🐳 Running with Docker (Recommended for Evaluators)

We provide optimized configurations to run the entire system inside Docker containers instantly, without needing local Python or PostgreSQL installations.

### 1. Development Mode (Includes PostgreSQL Database Container)
This builds the application and spins up a dedicated PostgreSQL database container connected automatically. It also mounts a code volume for live reloading.

```bash
# Start the development containers:
docker compose -f docker-compose.dev.yml up --build
```
* Once started, the API will be available at **`http://localhost:5000`** and Swagger specs at **`http://localhost:5000/swagger-ui`**.

### 2. Production Mode (Connects to External Database)
For production deployments, the application container starts standalone and connects to a production PostgreSQL instance provided via environmental configurations.

```bash
# Set your production database URL on your host system:
export DATABASE_URL="postgresql+asyncpg://<username>:<password>@<host>:5432/<db_name>"

# Run the production container:
docker compose -f docker-compose.prod.yml up --build
```

