import logging
from fastapi import FastAPI
from fastapi.exceptions import HTTPException

# logging
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi.exception_handlers import http_exception_handler
from core.routers.index import router as index_router

from core.configure_logging import configure_logging

logger = logging.getLogger(__name__)

app = FastAPI()
configure_logging()
logger.info("Starting FastAPI")
app.add_middleware(CorrelationIdMiddleware)

app.include_router(index_router)


# log all HTTP exception when raised
@app.exception_handler(HTTPException)
async def http_exception_handler_logging(request, exc):
    logger.error(f"HTTP Exception raised: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
