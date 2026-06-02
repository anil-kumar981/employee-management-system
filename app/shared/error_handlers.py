import logging
from flask import Flask, current_app
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from app.shared.exceptions import AppException
from app.shared.api_response.response_factory import ApiResponseFactory

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    """Register centralized error handlers to catch exceptions and return uniform JSON responses."""

    @app.errorhandler(AppException)
    def handle_app_exception(e: AppException):
        """Handle custom application layer exceptions (e.g. ValidationError, EntityNotFoundException)."""
        return ApiResponseFactory.error(
            message=e.message, errors=e.payload, status_code=e.status_code
        )

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e: IntegrityError):
        """Handle database constraint violations (e.g. duplicate email)."""
        logger.warning(f"Database IntegrityError encountered: {str(e)}")
        return ApiResponseFactory.error(
            message="Database constraint validation failed. This typically occurs due to a duplicate unique record (such as an email address).",
            status_code=409,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        """Handle standard HTTP exceptions and schema validation issues."""
        # For schema validation errors, detail payload is stored in e.data['messages']
        errors = None
        message = e.description or "An HTTP exception occurred."

        if hasattr(e, "data") and isinstance(e.data, dict):
            errors = e.data.get("messages")
            if errors:
                message = (
                    "Input validation failed. Please check the request parameters."
                )

        return ApiResponseFactory.error(
            message=message, errors=errors, status_code=e.code or 400
        )

    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        """Catch-all for internal unexpected failures, hiding raw tracebacks from users while logging details."""
        current_app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
        return ApiResponseFactory.error(
            message="An unexpected server error occurred. Please contact the administrator.",
            status_code=500,
        )
