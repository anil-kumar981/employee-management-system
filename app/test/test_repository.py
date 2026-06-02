import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import date
from contextlib import asynccontextmanager
from app.model.employee import Employee
from app.repositories.employee_repository import EmployeeRepository

@pytest.fixture
def mock_session():
    """Create a mock for SQLAlchemy AsyncSession."""
    session = MagicMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.get = AsyncMock()
    session.execute = AsyncMock()
    session.delete = AsyncMock()
    session.merge = AsyncMock()
    session.flush = AsyncMock()
    return session

@pytest.fixture
def repo(mock_session):
    """Fixture supplying EmployeeRepository injected with mock get_db directly."""
    @asynccontextmanager
    async def fake_get_db():
        yield mock_session
    return EmployeeRepository(get_db=fake_get_db)

@pytest.fixture
def mock_employee():
    return Employee(
        id=1,
        name="Alice Tester",
        email="alice@test.com",
        department="Engineering",
        date_joined=date(2026, 6, 2)
    )

def test_add_employee(repo, mock_session, mock_employee):
    """Test adding an employee commits changes to session."""
    mock_session.refresh = AsyncMock()
    
    saved_employee = asyncio.run(repo.add(mock_employee))
    
    mock_session.add.assert_called_once_with(mock_employee)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_employee)
    assert saved_employee == mock_employee

def test_get_by_id(repo, mock_session, mock_employee):
    """Test fetching an employee by ID queries session.get."""
    mock_session.get.return_value = mock_employee
    
    result = asyncio.run(repo.get_by_id(1))
    
    mock_session.get.assert_called_once_with(Employee, 1)
    assert result == mock_employee

def test_get_by_email(repo, mock_session, mock_employee):
    """Test fetching an employee by email issues async select query."""
    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = mock_employee
    
    result = asyncio.run(repo.get_by_email("alice@test.com"))
    
    mock_session.execute.assert_called_once()
    assert result == mock_employee

def test_get_all(repo, mock_session, mock_employee):
    """Test retrieving all records via select query execution."""
    mock_result = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.all.return_value = [mock_employee]
    
    result = asyncio.run(repo.get_all())
    
    mock_session.execute.assert_called_once()
    assert result == [mock_employee]

def test_update_employee(repo, mock_session, mock_employee):
    """Test updating merges changes and commits to session."""
    mock_session.merge.return_value = mock_employee
    mock_session.refresh = AsyncMock()
    
    result = asyncio.run(repo.update(mock_employee))
    
    mock_session.merge.assert_called_once_with(mock_employee)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_employee)
    assert result == mock_employee

def test_delete_employee_success(repo, mock_session, mock_employee):
    """Test deleting a present record issues delete and commit on session."""
    mock_session.get.return_value = mock_employee
    
    result = asyncio.run(repo.delete(1))
    
    mock_session.get.assert_called_once_with(Employee, 1)
    mock_session.delete.assert_called_once_with(mock_employee)
    mock_session.commit.assert_called_once()
    assert result is True

def test_delete_employee_missing(repo, mock_session):
    """Test deleting a missing record returns False and does not issue delete."""
    mock_session.get.return_value = None
    
    result = asyncio.run(repo.delete(99))
    
    mock_session.get.assert_called_once_with(Employee, 99)
    mock_session.delete.assert_not_called()
    assert result is False
