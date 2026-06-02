from app.repositories.base_repository import BaseEmployeeRepository
from app.repositories.employee_repository import SQLEmployeeRepository
from app.services.base_service import BaseEmployeeService
from app.services.employee_service import EmployeeServiceImpl

# Centralized instantiations to satisfy Dependency Injection
_employee_repository: BaseEmployeeRepository = SQLEmployeeRepository()
_employee_service: BaseEmployeeService = EmployeeServiceImpl(_employee_repository)

def get_employee_repository() -> BaseEmployeeRepository:
    """Dependency provider yielding a BaseEmployeeRepository instance."""
    return _employee_repository

def get_employee_service() -> BaseEmployeeService:
    """Dependency provider yielding a BaseEmployeeService instance."""
    return _employee_service
