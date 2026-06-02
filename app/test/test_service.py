import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import date
from app.model.employee import Employee
from app.services.employee_service import EmployeeServiceImpl
from app.shared.exceptions import ValidationError, ConflictException, EntityNotFoundException

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return EmployeeServiceImpl(mock_repo)

@pytest.fixture
def sample_payload():
    return {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "department": "HR",
        "date_joined": "2026-06-01"
    }

@pytest.fixture
def db_employee():
    return Employee(
        id=10,
        name="Jane Doe",
        email="jane@example.com",
        department="HR",
        date_joined=date(2026, 6, 1)
    )

def test_create_employee_success(service, mock_repo, sample_payload, db_employee):
    """Test successful employee registration."""
    # Setup mocks
    mock_repo.get_by_email = AsyncMock(return_value=None)
    mock_repo.add = AsyncMock(return_value=db_employee)
    
    result = asyncio.run(service.create_employee(sample_payload))
    
    mock_repo.get_by_email.assert_called_once_with("jane@example.com")
    mock_repo.add.assert_called_once()
    assert result["id"] == 10
    assert result["name"] == "Jane Doe"
    assert result["email"] == "jane@example.com"

def test_create_employee_validation_failure(service, mock_repo):
    """Test validation errors for invalid payloads (e.g. empty name, invalid email)."""
    invalid_payload = {
        "name": "   ",  # Blank space should raise validation error
        "email": "not-an-email",
        "department": "Engineering",
        "date_joined": "invalid-date"
    }
    
    with pytest.raises(ValidationError) as excinfo:
        asyncio.run(service.create_employee(invalid_payload))
        
    assert "Validation failed" in str(excinfo.value)
    # Assert specific field error reporting in payload
    assert "name" in excinfo.value.payload
    assert "email" in excinfo.value.payload
    assert "date_joined" in excinfo.value.payload

def test_create_employee_duplicate_email(service, mock_repo, sample_payload, db_employee):
    """Test that duplicate email registration raises ConflictException."""
    mock_repo.get_by_email = AsyncMock(return_value=db_employee)
    
    with pytest.raises(ConflictException) as excinfo:
        asyncio.run(service.create_employee(sample_payload))
        
    assert "already exists" in str(excinfo.value)
    mock_repo.add.assert_not_called()

def test_get_employee_by_id_success(service, mock_repo, db_employee):
    """Test successful lookup by ID."""
    mock_repo.get_by_id = AsyncMock(return_value=db_employee)
    
    result = asyncio.run(service.get_employee_by_id(10))
    
    mock_repo.get_by_id.assert_called_once_with(10)
    assert result["id"] == 10

def test_get_employee_by_id_missing(service, mock_repo):
    """Test lookup of non-existent ID raises EntityNotFoundException."""
    mock_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(EntityNotFoundException) as excinfo:
        asyncio.run(service.get_employee_by_id(99))
        
    assert "not found" in str(excinfo.value)

def test_update_employee_success(service, mock_repo, db_employee):
    """Test modifying employee details successfully (partial update)."""
    mock_repo.get_by_id = AsyncMock(return_value=db_employee)
    mock_repo.get_by_email = AsyncMock(return_value=None)
    
    # Save the updated model mock returns
    updated_model = Employee(
        id=10,
        name="Jane Updated",
        email="jane.new@example.com",
        department="HR",
        date_joined=date(2026, 6, 1)
    )
    mock_repo.update = AsyncMock(return_value=updated_model)
    
    update_data = {
        "name": "Jane Updated",
        "email": "jane.new@example.com"
    }
    
    result = asyncio.run(service.update_employee(10, update_data))
    
    assert result["name"] == "Jane Updated"
    assert result["email"] == "jane.new@example.com"
    mock_repo.update.assert_called_once()

def test_update_employee_duplicate_email(service, mock_repo, db_employee):
    """Test updating to an email that is already owned by another employee raises ConflictException."""
    mock_repo.get_by_id = AsyncMock(return_value=db_employee)
    
    another_employee = Employee(id=20, name="Other", email="other@example.com", department="IT", date_joined=date(2026, 1, 1))
    mock_repo.get_by_email = AsyncMock(return_value=another_employee)
    
    update_data = {
        "email": "other@example.com"
    }
    
    with pytest.raises(ConflictException) as excinfo:
        asyncio.run(service.update_employee(10, update_data))
        
    assert "already exists" in str(excinfo.value)

def test_delete_employee_success(service, mock_repo, db_employee):
    """Test deleting active employee."""
    mock_repo.get_by_id = AsyncMock(return_value=db_employee)
    mock_repo.delete = AsyncMock(return_value=True)
    
    result = asyncio.run(service.delete_employee(10))
    
    mock_repo.get_by_id.assert_called_once_with(10)
    mock_repo.delete.assert_called_once_with(10)
    assert result is True

def test_delete_employee_missing(service, mock_repo):
    """Test deleting missing employee raises EntityNotFoundException."""
    mock_repo.get_by_id = AsyncMock(return_value=None)
    
    with pytest.raises(EntityNotFoundException):
        asyncio.run(service.delete_employee(99))
        
    mock_repo.delete.assert_not_called()
