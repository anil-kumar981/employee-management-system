from typing import List, Dict, Any
from app.model.employee import Employee
from app.services.interface.iemployee_service import IEmployeeService
from app.shared.exceptions import ConflictException, EntityNotFoundException
from app.schema.employee import EmployeeCreateSchema, EmployeeUpdateSchema
from app.repositories.interface.iemployee_repository import IEmployeeRepo
from app.repositories.employee_repository import EmployeeRepository


class EmployeeServiceImpl(IEmployeeService):
    """Concrete service containing core business logic for managing Employees."""

    def __init__(self, repo: IEmployeeRepo = None) -> None:
        self.repo = repo or EmployeeRepository()

    async def create_employee(
        self, employee_in: EmployeeCreateSchema
    ) -> Dict[str, Any]:
        """Perform unique validation checks and add a new employee."""
        # 1. Assert unique email constraint in the business layer
        existing = await self.repo.get_by_email(employee_in.email)
        if existing:
            raise ConflictException(
                message=f"An employee with email '{employee_in.email}' already exists in the system."
            )

        # 2. Instantiate domain model and save via repository
        employee = Employee(
            name=employee_in.name,
            email=employee_in.email,
            department=employee_in.department,
            date_joined=employee_in.date_joined,
        )
        saved_employee = await self.repo.add(employee)
        return saved_employee.to_dict()

    async def get_employee_by_id(self, employee_id: int) -> Dict[str, Any]:
        """Fetch employee details by ID, raising EntityNotFoundException if missing."""
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(
                message=f"Employee with ID {employee_id} was not found in the database."
            )
        return employee.to_dict()

    async def get_all_employees(self) -> List[Dict[str, Any]]:
        """Retrieve all employees."""
        employees = await self.repo.get_all()
        return [emp.to_dict() for emp in employees]

    async def update_employee(
        self, employee_id: int, employee_in: EmployeeUpdateSchema
    ) -> Dict[str, Any]:
        """Validate and modify an existing employee's details."""
        # Verify existence of the employee
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(
                message=f"Cannot update employee. Employee with ID {employee_id} does not exist."
            )

        # Extract fields explicitly provided in the request payload
        update_data = employee_in.model_dump(exclude_unset=True)

        # Check for unique email conflicts if it is being changed
        if "email" in update_data:
            new_email = update_data["email"]
            if new_email != employee.email:
                existing = await self.repo.get_by_email(new_email)
                if existing:
                    raise ConflictException(
                        message=f"Cannot update email. An employee with email '{new_email}' already exists."
                    )

        # Modify fields
        for key, value in update_data.items():
            setattr(employee, key, value)

        # Commit modifications via repository
        updated_employee = await self.repo.update(employee)
        return updated_employee.to_dict()

    async def delete_employee(self, employee_id: int) -> bool:
        """Remove an employee record from the system, raising EntityNotFoundException if missing."""
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(
                message=f"Cannot delete employee. Employee with ID {employee_id} does not exist."
            )
        return await self.repo.delete(employee_id)
