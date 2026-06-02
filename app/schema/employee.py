from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class EmployeeBaseSchema(BaseModel):
    """Base schema outlining standard fields and formats for Employee."""
    name: str = Field(..., min_length=1, max_length=100, description="The full name of the employee")
    email: EmailStr = Field(..., description="The unique email address of the employee")
    department: str = Field(..., min_length=1, max_length=100, description="The department the employee belongs to")
    date_joined: date = Field(..., description="The date when the employee joined the company (YYYY-MM-DD)")

    @field_validator("name", "department")
    @classmethod
    def prevent_empty_whitespace(cls, value: str) -> str:
        """Ensure fields do not consist strictly of whitespace."""
        if not value.strip():
            raise ValueError("Field cannot be empty or contain only whitespace.")
        return value.strip()

class EmployeeCreateSchema(EmployeeBaseSchema):
    """Schema used during employee record creation."""
    pass

class EmployeeUpdateSchema(BaseModel):
    """Schema used during employee record modification, allowing partial inputs."""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="The updated name")
    email: Optional[EmailStr] = Field(None, description="The updated email address")
    department: Optional[str] = Field(None, min_length=1, max_length=100, description="The updated department")
    date_joined: Optional[date] = Field(None, description="The updated join date (YYYY-MM-DD)")

    @field_validator("name", "department")
    @classmethod
    def prevent_empty_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Ensure fields do not consist strictly of whitespace when provided."""
        if value is not None:
            if not value.strip():
                raise ValueError("Field cannot be empty or contain only whitespace.")
            return value.strip()
        return value

class EmployeeResponseSchema(EmployeeBaseSchema):
    """Schema representing serializable output for an Employee."""
    id: int

    model_config = {
        "from_attributes": True  # Enables direct conversion from SQLAlchemy ORM objects
    }
