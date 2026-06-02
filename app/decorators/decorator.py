from functools import wraps
import inspect
from flask import request
from pydantic import BaseModel, ValidationError as PydanticValidationError
from app.shared.exceptions import ValidationError

def validate_request(schema: type[BaseModel]):
    """Flask decorator validating incoming JSON payloads against a Pydantic schema.
    
    Supports both synchronous and asynchronous decorated view functions.
    If validation passes, the fully parsed and typed Pydantic model is injected 
    into the route function parameters as a keyword argument named 'body'.
    If validation fails, a semantic ValidationError containing field-specific errors is raised.
    """
    def decorator(f):
        if inspect.iscoroutinefunction(f):
            @wraps(f)
            async def async_wrapper(*args, **kwargs):
                json_data = request.get_json(silent=True)
                if json_data is None:
                    raise ValidationError(
                        message="Request body is missing or is not valid JSON.",
                        payload={"body": "Missing JSON body"}
                    )
                
                try:
                    # Validate and construct Pydantic model
                    validated_model = schema(**json_data)
                except PydanticValidationError as e:
                    # Extract clean, field-specific error messages
                    error_details = {str(err["loc"][0]): err["msg"] for err in e.errors()}
                    raise ValidationError(
                        message=f"Validation failed: {', '.join(error_details.values())}",
                        payload=error_details
                    )
                    
                # Inject validated Pydantic model as 'body' keyword parameter
                kwargs["body"] = validated_model
                return await f(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(f)
            def sync_wrapper(*args, **kwargs):
                json_data = request.get_json(silent=True)
                if json_data is None:
                    raise ValidationError(
                        message="Request body is missing or is not valid JSON.",
                        payload={"body": "Missing JSON body"}
                    )
                
                try:
                    # Validate and construct Pydantic model
                    validated_model = schema(**json_data)
                except PydanticValidationError as e:
                    # Extract clean, field-specific error messages
                    error_details = {str(err["loc"][0]): err["msg"] for err in e.errors()}
                    raise ValidationError(
                        message=f"Validation failed: {', '.join(error_details.values())}",
                        payload=error_details
                    )
                    
                # Inject validated Pydantic model as 'body' keyword parameter
                kwargs["body"] = validated_model
                return f(*args, **kwargs)
            return sync_wrapper
    return decorator
