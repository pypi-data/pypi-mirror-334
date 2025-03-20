import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("Logging Middleware")

class ProcessTimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request:Request, call_next):
        response = await call_next(request) #* Process the request and get the response
        logger.info(f"Request | Host: {request.client.host} | Port: {request.client.port} | Method: {request.method} | Path Params: {request.path_params} | Query Params: {request.query_params} | Status: {response.status_code}")
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            # client_ip = x_forwarded_for.split(",")[0]  # Get first IP in case of multiple
            client_ip = x_forwarded_for
            print("Got X-Forwarded-For |", "IP:", client_ip)
        else:
            client_ip = request.client.host  # Fallback to direct connection IP
            print("Direct Connection |", "IP:", client_ip)
        return response

def add_logging_middleware(app:FastAPI) -> None:
    """
    Adds Logging middleware to the FastAPI application.

    This middleware always logs any request and response.

    Args:
        app: FastAPI
            The FastAPI application instance to which the middleware will be added.

    Returns:
        None: The function modifies the FastAPI app by adding Logging middleware.

    Example:
    ```python
    add_logging_middleware(app=app)
    ```
    """
    app.add_middleware(ProcessTimeMiddleware)