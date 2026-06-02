import asyncio
from typing import List, Optional
from app.core.database import db
from app.model.employee import Employee
from app.repositories.base_repository import BaseEmployeeRepository

class SQLEmployeeRepository(BaseEmployeeRepository):
    """Concrete Employee repository implementing DB CRUD using SQLAlchemy.
    
    All operations are wrapped with `asyncio.to_thread` to run synchronously in a separate
    background worker thread, preventing blocks on the main async event loop.
    """
    
    async def add(self, employee: Employee) -> Employee:
        """Add a new employee to the database and commit."""
        def _add() -> Employee:
            db.session.add(employee)
            db.session.commit()
            return employee
        return await asyncio.to_thread(_add)
        
    async def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Fetch employee details by ID."""
        def _get() -> Optional[Employee]:
            return db.session.get(Employee, employee_id)
        return await asyncio.to_thread(_get)
        
    async def get_by_email(self, email: str) -> Optional[Employee]:
        """Fetch employee details by unique email."""
        def _get_by_email() -> Optional[Employee]:
            return db.session.query(Employee).filter(Employee.email == email).first()
        return await asyncio.to_thread(_get_by_email)
        
    async def get_all(self) -> List[Employee]:
        """Fetch all employees from the database."""
        def _get_all() -> List[Employee]:
            return db.session.query(Employee).all()
        return await asyncio.to_thread(_get_all)
        
    async def update(self, employee: Employee) -> Employee:
        """Commit structural modifications made to the model instance."""
        def _update() -> Employee:
            db.session.commit()
            return employee
        return await asyncio.to_thread(_update)
        
    async def delete(self, employee_id: int) -> bool:
        """Find an employee by ID and delete them, committing the action."""
        def _delete() -> bool:
            employee = db.session.get(Employee, employee_id)
            if employee:
                db.session.delete(employee)
                db.session.commit()
                return True
            return False
        return await asyncio.to_thread(_delete)
