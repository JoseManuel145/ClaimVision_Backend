import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from src.core.config import settings


def setup_logging() -> None:
    """Configura el sistema de logging de toda la app."""

    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))

    app_logger = logging.getLogger("ClaimVision")
    app_logger.setLevel(settings.LOG_LEVEL)
    app_logger.addHandler(handler)
    app_logger.propagate = False

    log_dir = "/app/logs"
    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "backend.log"),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    app_logger.addHandler(file_handler)

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """
    Cada módulo llama esto para obtener su logger con nombre jerárquico.
    Ejemplo: get_logger("usuarios.use_cases.create_usuario")
    """
    return logging.getLogger(f"ClaimVision.{name}")