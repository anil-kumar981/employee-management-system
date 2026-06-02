from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseEmployeeService(ABC):
    """Abstract interface defining business logic contract operations for managing Employees."""
    
    @abstractmethod
    async def create_employee(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform validation and add a new employee."""
        pass
        
    @abstractmethod
    async def get_employee_by_id(self, employee_id: int) -> Dict[str, Any]:
        """Retrieve a specific employee's details."""
        pass
        
    @abstractmethod
    async def get_all_employees(self) -> List[Dict[str, Any]]:
        """Retrieve all employees' details."""
        pass
        
    @abstractmethod
    async def update_employee(self, employee_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and modify an existing employee's details."""
        pass
        
    @abstractmethod
    async def delete_employee(self, employee_id: int) -> bool:
        """Remove an employee record from the system."""
        pass
