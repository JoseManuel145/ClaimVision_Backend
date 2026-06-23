import logging
import sys

from src.core.config import settings


def setup_logging() -> None:
    """Configura el sistema de logging de toda la app."""

    # Formato legible en desarrollo, fácil de parsear en producción
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Handler principal — siempre a stdout (buena práctica en APIs)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))

    # Logger raíz de tu app — todos los módulos heredan de este
    app_logger = logging.getLogger("ClaimVision")
    app_logger.setLevel(settings.LOG_LEVEL)  # viene del .env
    app_logger.addHandler(handler)
    app_logger.propagate = False  # no duplica logs al logger raíz de Python

    # Silencias librerías ruidosas pero conservas sus warnings/errors
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