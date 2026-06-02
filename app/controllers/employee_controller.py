import asyncio
from flask.views import MethodView
from flask_smorest import Blueprint
from app.dependencies.container import get_employee_service
from app.schema.marshmallow_schemas import (
    EmployeeCreateMSchema,
    EmployeeUpdateMSchema,
    EmployeeResponseWrapperSchema,
    EmployeeListResponseWrapperSchema,
    ApiResponseMSchema
)
from app.shared.response_factory import ApiResponseFactory

# Setup Smorest Blueprint for Employee routing
blp = Blueprint(
    name="employees", 
    import_name="employees", 
    url_prefix="/employees", 
    description="Operations on employee records, structured in a layered DI architecture."
)

@blp.route("/")
class EmployeesRoot(MethodView):
    """Router class handling collection endpoints for Employees."""
    
    @blp.response(200, EmployeeListResponseWrapperSchema)
    def get(self):
        """Retrieve list of all employees.
        
        Fetches all registered employee records. Returns a custom-wrapped JSON array.
        """
        service = get_employee_service()
        employees = asyncio.run(service.get_all_employees())
        message = f"Successfully retrieved {len(employees)} employee record{'s' if len(employees) != 1 else ''}."
        return ApiResponseFactory.success(employees, message)

    @blp.arguments(EmployeeCreateMSchema)
    @blp.response(201, EmployeeResponseWrapperSchema)
    def post(self, employee_data: dict):
        """Add a new employee.
        
        Validates the request parameters, ensures the email address is unique,
        creates a new employee, and registers them in the system database.
        """
        service = get_employee_service()
        employee = asyncio.run(service.create_employee(employee_data))
        message = f"Employee '{employee['name']}' was successfully created with ID {employee['id']}."
        return ApiResponseFactory.success(employee, message, 201)

@blp.route("/<int:id>")
class EmployeesById(MethodView):
    """Router class handling individual entity endpoints for Employees."""

    @blp.response(200, EmployeeResponseWrapperSchema)
    def get(self, id: int):
        """Retrieve details of a specific employee.
        
        Fetches a single employee record matching the given unique identifier.
        """
        service = get_employee_service()
        employee = asyncio.run(service.get_employee_by_id(id))
        message = f"Employee details for ID {id} ('{employee['name']}') successfully retrieved."
        return ApiResponseFactory.success(employee, message)

    @blp.arguments(EmployeeUpdateMSchema)
    @blp.response(200, EmployeeResponseWrapperSchema)
    def put(self, employee_data: dict, id: int):
        """Update an existing employee's information.
        
        Modifies fields provided in the body payload (partial updates are supported).
        Ensures email uniqueness checks are not bypassed.
        """
        service = get_employee_service()
        employee = asyncio.run(service.update_employee(id, employee_data))
        message = f"Employee '{employee['name']}' (ID {id}) was successfully updated."
        return ApiResponseFactory.success(employee, message)

    @blp.response(200, ApiResponseMSchema)
    def delete(self, id: int):
        """Remove an employee from the system.
        
        Permanently deletes the employee matching the ID parameter from the database.
        """
        service = get_employee_service()
        asyncio.run(service.delete_employee(id))
        message = f"Employee with ID {id} was successfully removed from the system."
        return ApiResponseFactory.success(None, message)
