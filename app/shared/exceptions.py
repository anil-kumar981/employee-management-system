from typing import Any, Dict, Optional

class AppException(Exception):
    """Base application exception for custom error handling."""
    status_code: int = 500
    
    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.payload = payload

class EntityNotFoundException(AppException):
    """Raised when a requested resource does not exist in the system."""
    status_code: int = 404

class ValidationError(AppException):
    """Raised when data validations fail in the service or schema layers."""
    status_code: int = 400

class ConflictException(AppException):
    """Raised when an operation conflicts with existing server state (e.g., unique email constraint violation)."""
    status_code: int = 409

class DatabaseException(AppException):
    """Raised when an unexpected database operations error occurs."""
    status_code: int = 500
