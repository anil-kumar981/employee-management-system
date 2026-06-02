import asyncio
import pytest
from unittest.mock import MagicMock, patch
from datetime import date
from app.model.employee import Employee
from app.repositories.employee_repository import SQLEmployeeRepository

@pytest.fixture
def repo():
    return SQLEmployeeRepository()

@pytest.fixture
def mock_employee():
    return Employee(
        id=1,
        name="Alice Tester",
        email="alice@test.com",
        department="Engineering",
        date_joined=date(2026, 6, 2)
    )

def test_add_employee(repo, mock_employee):
    """Test adding an employee commits the changes to the database."""
    with patch("app.repositories.employee_repository.db.session") as mock_session:
        # Execute async method synchronously using asyncio.run
        saved_employee = asyncio.run(repo.add(mock_employee))
        
        mock_session.add.assert_called_once_with(mock_employee)
        mock_session.commit.assert_called_once()
        assert saved_employee == mock_employee

def test_get_by_id(repo, mock_employee):
    """Test fetching an employee by ID queries db.session.get."""
    with patch("app.repositories.employee_repository.db.session") as mock_session:
        mock_session.get.return_value = mock_employee
        
        result = asyncio.run(repo.get_by_id(1))
        
        mock_session.get.assert_called_once_with(Employee, 1)
        assert result == mock_employee

def test_get_by_email(repo, mock_employee):
    """Test fetching an employee by email issues query filtering."""
    with patch("app.repositories.employee_repository.db.session") as mock_session:
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_filter = MagicMock()
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = mock_employee
        
        result = asyncio.run(repo.get_by_email("alice@test.com"))
        
        mock_session.query.assert_called_once_with(Employee)
        mock_filter.first.assert_called_once()
        assert result == mock_employee

def test_get_all(repo, mock_employee):
    """Test retrieving all records."""
    with patch("app.repositories.employee_repository.db.session") as mock_session:
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query
        mock_query.all.return_value = [mock_employee]
        
        result = asyncio.run(repo.get_all())
        
        mock_session.query.assert_called_once_with(Employee)
        assert result == [mock_employee]

def test_update_employee(repo, mock_employee):
    """Test updating commits the active session transaction."""
    with patch("app.repositories.employee_repository.db.session") as mock_session:
        result = asyncio.run(repo.update(mock_employee))
        
        mock_session.commit.assert_called_once()
        assert result == mock_employee

def test_delete_employee_success(repo, mock_employee):
    """Test deleting a present record removes and commits."""
    with patch("app.repositories.employee_repository.db.session") as mock_session:
        mock_session.get.return_value = mock_employee
        
        result = asyncio.run(repo.delete(1))
        
        mock_session.get.assert_called_once_with(Employee, 1)
        mock_session.delete.assert_called_once_with(mock_employee)
        mock_session.commit.assert_called_once()
        assert result is True

def test_delete_employee_missing(repo):
    """Test deleting a missing record returns False and does not issue delete."""
    with patch("app.repositories.employee_repository.db.session") as mock_session:
        mock_session.get.return_value = None
        
        result = asyncio.run(repo.delete(99))
        
        mock_session.get.assert_called_once_with(Employee, 99)
        mock_session.delete.assert_not_called()
        assert result is False
