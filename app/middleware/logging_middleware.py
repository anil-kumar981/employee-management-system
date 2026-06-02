import time
import logging
from flask import Flask, request

# Setup standard logger
logger = logging.getLogger("app.api")
logger.setLevel(logging.INFO)

# Ensure handler exists and outputs cleanly to Stream
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class APILoggingMiddleware:
    """
    Middleware to log every incoming API request and outgoing response,
    including execution time, request path, HTTP method, client IP, and status code.
    """
    def __init__(self, app: Flask = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        @app.before_request
        def start_timer():
            request.start_time = time.time()

        @app.after_request
        def log_request_response(response):
            # Calculate execution duration
            if hasattr(request, 'start_time'):
                process_time = time.time() - request.start_time
            else:
                process_time = 0.0

            # Gather request metadata
            client_ip = request.remote_addr or "unknown"
            method = request.method
            path = request.path
            query = f"?{request.query_string.decode('utf-8')}" if request.query_string else ""
            status_code = response.status_code

            # Determine severity and format the log message
            if status_code >= 400:
                logger.warning(
                    f'{client_ip} - "{method} {path}{query}" {status_code} FAILURE | Duration: {process_time:.3f}s'
                )
            else:
                logger.info(
                    f'{client_ip} - "{method} {path}{query}" {status_code} SUCCESS | Duration: {process_time:.3f}s'
                )

            return response
