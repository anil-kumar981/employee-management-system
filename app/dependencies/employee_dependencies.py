from app.services.interface.iemployee_service import IEmployeeService
from app.services.employee_service import EmployeeServiceImpl
from app.repositories.interface.iemployee_repository import IEmployeeRepo
from app.repositories.employee_repository import EmployeeRepository

# 1. Instantiate the Repository once
_employee_repo: IEmployeeRepo = EmployeeRepository()

# 2. Instantiate the Service, injecting the repository instance directly
_employee_service: IEmployeeService = EmployeeServiceImpl(repo=_employee_repo)

def get_employee_service() -> IEmployeeService:
    """Dependency provider yielding an IEmployeeService instance."""
    return _employee_service
