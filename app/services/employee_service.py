from typing import List, Dict, Any
from pydantic import ValidationError as PydanticValidationError
from app.model.employee import Employee
from app.repositories.base_repository import BaseEmployeeRepository
from app.services.base_service import BaseEmployeeService
from app.shared.exceptions import ValidationError, ConflictException, EntityNotFoundException
from app.schema.employee import EmployeeCreateSchema, EmployeeUpdateSchema

class EmployeeServiceImpl(BaseEmployeeService):
    """Concrete service containing core business logic for managing Employees.
    
    Adheres to dependency injection by accepting an abstract BaseEmployeeRepository instance.
    """
    
    def __init__(self, employee_repository: BaseEmployeeRepository) -> None:
        self.repo = employee_repository
        
    async def create_employee(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform validation and add a new employee."""
        # 1. Run rigorous schema and type validations via Pydantic
        try:
            validated_data = EmployeeCreateSchema(**data)
        except PydanticValidationError as e:
            # Flatten Pydantic errors into key-value descriptions and raise custom ValidationError
            error_details = {str(err["loc"][0]): err["msg"] for err in e.errors()}
            raise ValidationError(
                message=f"Validation failed: {', '.join(error_details.values())}",
                payload=error_details
            )
            
        # 2. Assert unique email constraint in the business layer
        existing = await self.repo.get_by_email(validated_data.email)
        if existing:
            raise ConflictException(
                message=f"An employee with email '{validated_data.email}' already exists in the system."
            )
            
        # 3. Instantiate domain model and commit via repository
        employee = Employee(
            name=validated_data.name,
            email=validated_data.email,
            department=validated_data.department,
            date_joined=validated_data.date_joined
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
        
    async def update_employee(self, employee_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and modify an existing employee's details."""
        # 1. Verify existence of the employee
        employee = await self.repo.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(
                message=f"Cannot update employee. Employee with ID {employee_id} does not exist."
            )
            
        # 2. Run validations for fields provided (allowing partial updates)
        try:
            validated_data = EmployeeUpdateSchema(**data)
        except PydanticValidationError as e:
            error_details = {str(err["loc"][0]): err["msg"] for err in e.errors()}
            raise ValidationError(
                message=f"Update validation failed: {', '.join(error_details.values())}",
                payload=error_details
            )
            
        # 3. Check for unique email conflicts if it is being changed
        if validated_data.email is not None and validated_data.email != employee.email:
            existing = await self.repo.get_by_email(validated_data.email)
            if existing:
                raise ConflictException(
                    message=f"Cannot update email. An employee with email '{validated_data.email}' already exists."
                )
            employee.email = validated_data.email
            
        # 4. Modify fields
        if validated_data.name is not None:
            employee.name = validated_data.name
        if validated_data.department is not None:
            employee.department = validated_data.department
        if validated_data.date_joined is not None:
            employee.date_joined = validated_data.date_joined
            
        # 5. Commit modifications via repository
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
