from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union, Tuple
from app.schema.employee import EmployeeCreateSchema, EmployeeUpdateSchema

class IEmployeeService(ABC):
    """Interface declaring business logic contract operations for managing Employees."""
    
    @abstractmethod
    async def create_employee(self, employee_in: EmployeeCreateSchema) -> Dict[str, Any]:
        """Perform validation and add a new employee."""
        pass
        
    @abstractmethod
    async def get_employee_by_id(self, employee_id: int) -> Dict[str, Any]:
        """Retrieve a specific employee's details."""
        pass
        
    @abstractmethod
    async def get_all_employees(self, params: Optional[Dict[str, Any]] = None) -> Union[List[Dict[str, Any]], Tuple[List[Dict[str, Any]], Dict[str, Any]]]:
        """Retrieve all employees' details, optionally applying pagination, sorting, and searching."""
        pass
        
    @abstractmethod
    async def update_employee(self, employee_id: int, employee_in: EmployeeUpdateSchema) -> Dict[str, Any]:
        """Validate and modify an existing employee's details."""
        pass
        
    @abstractmethod
    async def delete_employee(self, employee_id: int) -> bool:
        """Remove an employee record from the system."""
        pass
