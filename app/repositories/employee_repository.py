from typing import Optional
from sqlalchemy import select
from app.model.employee import Employee
from app.repositories.base_repository import BaseRepo
from app.repositories.interface.iemployee_repository import IEmployeeRepo
from app.database.database import get_db

class EmployeeRepository(BaseRepo[Employee], IEmployeeRepo):
    """Concrete repository implementing Employee-specific database access natively using SQLAlchemy sessions."""
    
    def __init__(self, get_db=get_db) -> None:
        super().__init__(Employee, get_db=get_db)
        
    async def get_by_email(self, email: str) -> Optional[Employee]:
        """Fetch employee details by their unique email."""
        async with self.get_db() as session:
            result = await session.execute(select(Employee).filter(Employee.email == email))
            return result.scalars().first()
