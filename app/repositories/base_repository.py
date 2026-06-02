from abc import ABC, abstractmethod
from typing import List, Optional
from app.model.employee import Employee

class BaseEmployeeRepository(ABC):
    """Abstract interface defining required database contract operations for Employee data access."""
    
    @abstractmethod
    async def add(self, employee: Employee) -> Employee:
        """Add a new employee to the database."""
        pass
        
    @abstractmethod
    async def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Retrieve an employee by their ID."""
        pass
        
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Employee]:
        """Retrieve an employee by their unique email."""
        pass
        
    @abstractmethod
    async def get_all(self) -> List[Employee]:
        """Retrieve all employee records."""
        pass
        
    @abstractmethod
    async def update(self, employee: Employee) -> Employee:
        """Save updates to an existing employee."""
        pass
        
    @abstractmethod
    async def delete(self, employee_id: int) -> bool:
        """Remove an employee record by their ID."""
        pass
