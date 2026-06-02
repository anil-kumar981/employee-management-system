import marshmallow as ma

class EmployeeMSchema(ma.Schema):
    """Marshmallow schema representing an Employee response object for Swagger documentation."""
    id = ma.fields.Int(dump_only=True, metadata={"description": "The unique identifier of the employee record."})
    name = ma.fields.Str(required=True, validate=ma.validate.Length(min=1, max=100), metadata={"description": "The full name of the employee."})
    email = ma.fields.Email(required=True, validate=ma.validate.Length(max=120), metadata={"description": "The unique email address of the employee."})
    department = ma.fields.Str(required=True, validate=ma.validate.Length(min=1, max=100), metadata={"description": "The department the employee belongs to."})
    date_joined = ma.fields.Date(required=True, metadata={"description": "The date when the employee joined the company (YYYY-MM-DD)."})

class EmployeeCreateMSchema(ma.Schema):
    """Marshmallow schema for creating an Employee, used in Swagger API validation."""
    name = ma.fields.Str(required=True, validate=ma.validate.Length(min=1, max=100), metadata={"description": "The full name of the employee."})
    email = ma.fields.Email(required=True, validate=ma.validate.Length(max=120), metadata={"description": "The unique email address of the employee."})
    department = ma.fields.Str(required=True, validate=ma.validate.Length(min=1, max=100), metadata={"description": "The department the employee belongs to."})
    date_joined = ma.fields.Date(required=True, metadata={"description": "The date when the employee joined the company (YYYY-MM-DD)."})

class EmployeeUpdateMSchema(ma.Schema):
    """Marshmallow schema for updating an Employee, used in Swagger API validation."""
    name = ma.fields.Str(required=False, validate=ma.validate.Length(min=1, max=100), metadata={"description": "The updated full name."})
    email = ma.fields.Email(required=False, validate=ma.validate.Length(max=120), metadata={"description": "The updated unique email."})
    department = ma.fields.Str(required=False, validate=ma.validate.Length(min=1, max=100), metadata={"description": "The updated department name."})
    date_joined = ma.fields.Date(required=False, metadata={"description": "The updated join date."})

class ApiResponseMSchema(ma.Schema):
    """General wrapped response schema structure for the application."""
    success = ma.fields.Bool(dump_only=True, metadata={"description": "Indicates if the operation was successful."})
    message = ma.fields.Str(dump_only=True, metadata={"description": "A dynamic descriptive message detailing the result."})

class EmployeeResponseWrapperSchema(ma.Schema):
    """Wrapped success response containing a single employee record."""
    success = ma.fields.Bool(dump_only=True)
    message = ma.fields.Str(dump_only=True)
    data = ma.fields.Nested(EmployeeMSchema)

class EmployeeListResponseWrapperSchema(ma.Schema):
    """Wrapped success response containing an array of employee records."""
    success = ma.fields.Bool(dump_only=True)
    message = ma.fields.Str(dump_only=True)
    data = ma.fields.Nested(EmployeeMSchema, many=True)

