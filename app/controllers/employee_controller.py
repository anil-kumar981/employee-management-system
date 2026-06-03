from flask import Blueprint, request
from app.dependencies.employee_dependencies import get_employee_service
from app.schema.employee import EmployeeCreateSchema, EmployeeUpdateSchema
from app.decorators.decorator import validate_request
from app.shared.api_response.response_factory import ApiResponseFactory

# Create a standard, vanilla Flask Blueprint for Employees routing
employee_bp = Blueprint("employees", __name__, url_prefix="/employees")


@employee_bp.route("/", methods=["GET"])
async def get_all_employees():
    """Retrieve list of all employees."""
    service = get_employee_service()
    params = request.args.to_dict()
    result = await service.get_all_employees(params)

    if isinstance(result, tuple):
        employees, paginated_meta = result
        total_count = paginated_meta["total_results"]
    else:
        employees = result
        paginated_meta = None
        total_count = len(employees)

    message = f"Successfully retrieved {total_count} employee record{'s' if total_count != 1 else ''}."
    return ApiResponseFactory.success(employees, message, paginated_meta=paginated_meta)


@employee_bp.route("/", methods=["POST"])
@validate_request(EmployeeCreateSchema)
async def create_employee(body: EmployeeCreateSchema):
    """Add a new employee, validating the incoming JSON against Pydantic."""
    service = get_employee_service()
    employee = await service.create_employee(body)
    message = f"Employee '{employee['name']}' was successfully created with ID {employee['id']}."
    return ApiResponseFactory.success(employee, message, 201)


@employee_bp.route("/<int:id>", methods=["GET"])
async def get_employee_by_id(id: int):
    """Retrieve details of a specific employee."""
    service = get_employee_service()
    employee = await service.get_employee_by_id(id)
    message = (
        f"Employee details for ID {id} ('{employee['name']}') successfully retrieved."
    )
    return ApiResponseFactory.success(employee, message)


@employee_bp.route("/<int:id>", methods=["PUT", "PATCH"])
@validate_request(EmployeeUpdateSchema)
async def update_employee(id: int, body: EmployeeUpdateSchema):
    """Update an existing employee's information, validating incoming JSON against Pydantic."""
    service = get_employee_service()
    employee = await service.update_employee(id, body)
    message = f"Employee '{employee['name']}' (ID {id}) was successfully updated."
    return ApiResponseFactory.success(employee, message)


@employee_bp.route("/<int:id>", methods=["DELETE"])
async def delete_employee(id: int):
    """Remove an employee from the system."""
    service = get_employee_service()
    await service.delete_employee(id)
    message = f"Employee with ID {id} was successfully removed from the system."
    return ApiResponseFactory.success(None, message)
