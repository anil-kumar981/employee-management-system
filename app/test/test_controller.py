import pytest
from unittest.mock import AsyncMock, patch
from app import create_app
from app.shared.exceptions import EntityNotFoundException


@pytest.fixture
def app():
    """Create Flask application configured for test execution."""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """Test client for issuing requests."""
    return app.test_client()


def test_get_all_employees_success(client):
    """Test retrieving employee collection maps to JSON success response."""
    with patch(
        "app.controllers.employee_controller.get_employee_service"
    ) as mock_get_service:
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        mock_service.get_all_employees.return_value = [
            {
                "id": 1,
                "name": "Bob Tester",
                "email": "bob@test.com",
                "department": "QA",
                "date_joined": "2026-06-01",
            }
        ]

        response = client.get("/employees/")
        assert response.status_code == 200

        body = response.get_json()
        assert body["success"] is True
        assert "Successfully retrieved 1 employee record" in body["message"]
        assert len(body["data"]) == 1
        assert body["data"][0]["name"] == "Bob Tester"


def test_create_employee_success(client):
    """Test creating an employee yields 201 status and dynamic confirmation message."""
    with patch(
        "app.controllers.employee_controller.get_employee_service"
    ) as mock_get_service:
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        mock_service.create_employee.return_value = {
            "id": 5,
            "name": "Alice Developer",
            "email": "alice@test.com",
            "department": "IT",
            "date_joined": "2026-06-02",
        }

        payload = {
            "name": "Alice Developer",
            "email": "alice@test.com",
            "department": "IT",
            "date_joined": "2026-06-02",
        }

        response = client.post("/employees/", json=payload)
        assert response.status_code == 201

        body = response.get_json()
        assert body["success"] is True
        assert (
            "Employee 'Alice Developer' was successfully created with ID 5"
            in body["message"]
        )
        assert body["data"]["id"] == 5


def test_get_employee_by_id_success(client):
    """Test fetching single employee by ID returns correct wrapped details."""
    with patch(
        "app.controllers.employee_controller.get_employee_service"
    ) as mock_get_service:
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        mock_service.get_employee_by_id.return_value = {
            "id": 10,
            "name": "Charlie Manager",
            "email": "charlie@test.com",
            "department": "Operations",
            "date_joined": "2026-05-15",
        }

        response = client.get("/employees/10")
        assert response.status_code == 200

        body = response.get_json()
        assert body["success"] is True
        assert "Charlie Manager" in body["message"]
        assert body["data"]["id"] == 10


def test_get_employee_by_id_not_found(client):
    """Test lookup of non-existent resource routes correctly to 404 handler."""
    with patch(
        "app.controllers.employee_controller.get_employee_service"
    ) as mock_get_service:
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        mock_service.get_employee_by_id.side_effect = EntityNotFoundException(
            "Employee with ID 99 was not found in the database."
        )

        response = client.get("/employees/99")
        assert response.status_code == 404

        body = response.get_json()
        assert body["success"] is False
        assert "not found" in body["message"]


def test_update_employee_success(client):
    """Test putting updates returns 200 and modification message."""
    with patch(
        "app.controllers.employee_controller.get_employee_service"
    ) as mock_get_service:
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        mock_service.update_employee.return_value = {
            "id": 10,
            "name": "Charlie Updated",
            "email": "charlie@test.com",
            "department": "Executive",
            "date_joined": "2026-05-15",
        }

        payload = {"name": "Charlie Updated", "department": "Executive"}
        response = client.patch("/employees/10", json=payload)
        assert response.status_code == 200

        body = response.get_json()
        assert body["success"] is True
        assert (
            "Employee 'Charlie Updated' (ID 10) was successfully updated."
            in body["message"]
        )
        assert body["data"]["department"] == "Executive"


def test_delete_employee_success(client):
    """Test deleting returns successful status and message wrapper."""
    with patch(
        "app.controllers.employee_controller.get_employee_service"
    ) as mock_get_service:
        mock_service = AsyncMock()
        mock_get_service.return_value = mock_service

        mock_service.delete_employee.return_value = True

        response = client.delete("/employees/10")
        assert response.status_code == 200

        body = response.get_json()
        assert body["success"] is True
        assert "removed from the system" in body["message"]


def test_invalid_post_payload_structure(client):
    """Test that posting completely un-parseable JSON payload causes Pydantic schema validation error."""
    response = client.post("/employees/", json={"bad_field": "some data"})
    assert (
        response.status_code == 400
    )  # Pydantic validation fails and returns Bad Request status

    body = response.get_json()
    assert body["success"] is False
    assert "validation failed" in body["message"].lower()
    assert "errors" in body
