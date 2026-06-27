import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger("http")

def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - {process_time:.4f}s")
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"{request.method} {request.url.path} - Exception: {str(e)} - {process_time:.4f}s")
            raise
