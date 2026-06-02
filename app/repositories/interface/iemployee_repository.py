from abc import abstractmethod
from typing import Optional
from app.model.employee import Employee
from app.repositories.interface.ibase_repository import IBaseRepo

class IEmployeeRepo(IBaseRepo[Employee]):
    """Interface declaring Employee-specific database operations."""
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Employee]:
        """Fetch employee details by their unique email."""
        pass
