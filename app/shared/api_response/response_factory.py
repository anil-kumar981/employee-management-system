from flask import jsonify
from typing import Any, Dict, Tuple, Optional

class ApiResponseFactory:
    """Factory for standard, dynamic, and clean JSON responses across the application."""
    
    @staticmethod
    def success(
        data: Optional[Any] = None, 
        message: str = "Operation completed successfully.", 
        status_code: int = 200
    ) -> Tuple[Any, int]:
        """Generate a success response."""
        response_body: Dict[str, Any] = {
            "success": True,
            "message": message
        }
        if data is not None:
            response_body["data"] = data
            
        return jsonify(response_body), status_code

    @staticmethod
    def error(
        message: str, 
        errors: Optional[Any] = None, 
        status_code: int = 400
    ) -> Tuple[Any, int]:
        """Generate an error response."""
        response_body: Dict[str, Any] = {
            "success": False,
            "message": message
        }
        if errors is not None:
            response_body["errors"] = errors
            
        return jsonify(response_body), status_code
