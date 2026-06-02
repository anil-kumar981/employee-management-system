from pydantic import BaseModel


class ApiResponseSchema(BaseModel):
    """Wrapped base response schema structure."""

    success: bool
    message: str
