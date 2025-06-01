from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import traceback
from brain_app.core.logging_config import logger

class ExceptionLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            tb_str = traceback.format_exc()
            logger.error(f"Unhandled error processing request {request.method} {request.url}:\n{tb_str}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )
