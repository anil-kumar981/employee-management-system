import pytest
from unittest.mock import patch, AsyncMock
from app import create_app


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


def test_middleware_logging_success(client):
    """Test that the middleware successfully logs a 200 SUCCESS message for successful requests."""
    with patch("app.middleware.logging_middleware.logger") as mock_logger:
        # Patch the controller service locator
        with patch(
            "app.controllers.employee_controller.get_employee_service"
        ) as mock_get_service:
            mock_service = AsyncMock()
            # Mock the async call wrapper's behavior for get_all_employees
            mock_service.get_all_employees.return_value = []
            mock_get_service.return_value = mock_service

            response = client.get("/employees/")
            assert response.status_code == 200

            # Verify logger.info was called with standard format containing SUCCESS
            mock_logger.info.assert_called_once()
            log_args = mock_logger.info.call_args[0][0]
            assert "GET /employees/" in log_args
            assert "200 SUCCESS" in log_args
            assert "Duration:" in log_args


def test_middleware_logging_failure(client):
    """Test that the middleware logs a warning/failure message for 400 Bad Request responses."""
    with patch("app.middleware.logging_middleware.logger") as mock_logger:
        # Sending an invalid POST body to trigger validation error (400)
        response = client.post("/employees/", json={"bad_field": "some data"})
        assert response.status_code == 400

        # Verify logger.warning was called with standard format containing FAILURE
        mock_logger.warning.assert_called_once()
        log_args = mock_logger.warning.call_args[0][0]
        assert "POST /employees/" in log_args
        assert "400 FAILURE" in log_args
        assert "Duration:" in log_args
