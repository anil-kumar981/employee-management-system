import re
from datetime import date, datetime
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field, field_validator
from .api_response_schema import ApiResponseSchema


class EmployeeBaseSchema(BaseModel):
    """Base schema outlining standard fields and formats for Employee."""

    name: str = Field(
        ..., min_length=1, max_length=100, description="The full name of the employee"
    )
    email: EmailStr = Field(..., description="The unique email address of the employee")
    department: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="The department the employee belongs to",
    )
    date_joined: date = Field(
        ..., description="The date when the employee joined the company (YYYY-MM-DD)"
    )

    @field_validator("name", "department")
    @classmethod
    def prevent_empty_whitespace(cls, value: str) -> str:
        """Ensure fields do not consist strictly of whitespace."""
        if not value.strip():
            raise ValueError("Field cannot be empty or contain only whitespace.")
        return value.strip()

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_format(cls, value: Any) -> Any:
        """Ensure email is provided in a valid, user-friendly format."""
        if value is None:
            return value
        if isinstance(value, str):
            email_val = value.strip()
            # Basic validation regex checking for user@domain.com
            email_regex = r"^[^@]+@[^@]+\.[^@]+$"
            if not re.match(email_regex, email_val):
                raise ValueError(
                    "Please enter a valid email address (e.g., xyz@gmail.com)."
                )
            return email_val
        return value

    @field_validator("date_joined", mode="before")
    @classmethod
    def validate_date_format(cls, value: Any) -> Any:
        """Ensure date is provided in strict YYYY-MM-DD format."""
        if value is None:
            return value
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    "Date must be in strict YYYY-MM-DD format (e.g., '2026-06-02')."
                )
        raise ValueError("Invalid date format.")


class EmployeeCreateSchema(EmployeeBaseSchema):
    """Schema used during employee record creation."""

    pass


class EmployeeUpdateSchema(BaseModel):
    """Schema used during employee record modification, allowing partial inputs."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="The updated name"
    )
    email: Optional[EmailStr] = Field(None, description="The updated email address")
    department: Optional[str] = Field(
        None, min_length=1, max_length=100, description="The updated department"
    )
    date_joined: Optional[date] = Field(
        None, description="The updated join date (YYYY-MM-DD)"
    )

    @field_validator("name", "email", "department", "date_joined", mode="before")
    @classmethod
    def prevent_nulls(cls, value: Any) -> Any:
        """Ensure fields cannot be explicitly set to null/None."""
        if value is None:
            raise ValueError("Field value cannot be null/None.")
        return value

    @field_validator("name", "department")
    @classmethod
    def prevent_empty_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Ensure fields do not consist strictly of whitespace when provided."""
        if value is not None:
            if not value.strip():
                raise ValueError("Field cannot be empty or contain only whitespace.")
            return value.strip()
        return value

    @field_validator("email", mode="before")
    @classmethod
    def validate_email_format(cls, value: Any) -> Any:
        """Ensure email is provided in a valid, user-friendly format."""
        if value is None:
            return value
        if isinstance(value, str):
            email_val = value.strip()
            email_regex = r"^[^@]+@[^@]+\.[^@]+$"
            if not re.match(email_regex, email_val):
                raise ValueError(
                    "Please enter a valid email address (e.g., xyz@example.com)."
                )
            return email_val
        return value

    @field_validator("date_joined", mode="before")
    @classmethod
    def validate_date_format(cls, value: Any) -> Any:
        """Ensure date is provided in strict YYYY-MM-DD format."""
        if value is None:
            return value
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(
                    "Date must be in strict YYYY-MM-DD format (e.g., '2026-06-02')."
                )
        raise ValueError("Invalid date format.")


class EmployeeResponseSchema(EmployeeBaseSchema):
    """Schema representing serializable output for an Employee."""

    id: int

    model_config = {
        "from_attributes": True  # Enables direct conversion from SQLAlchemy ORM objects
    }


class EmployeeResponseWrapperSchema(ApiResponseSchema):
    """Wrapped success response containing a single employee record."""

    data: EmployeeResponseSchema


class EmployeeListResponseWrapperSchema(ApiResponseSchema):
    """Wrapped success response containing an array of employee records."""

    data: list[EmployeeResponseSchema]
