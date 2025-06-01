from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
from brain_app.core.logging_config import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"MW - Recebida requisição {request.method} {request.url}")
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(f"MW - Resposta {response.status_code} em {duration:.2f}s")
        return response
