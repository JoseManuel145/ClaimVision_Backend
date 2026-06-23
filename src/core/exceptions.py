from typing import Any, Optional

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse, Response


# Errores comunes como subclases de HTTPException para lanzar directamente
class BadRequestError(HTTPException):
    """400 Bad Request - Datos inválidos: campos faltantes o formato incorrecto."""

    def __init__(self, detail: str = "Datos inválidos"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedError(HTTPException):
    """401 Unauthorized - Token ausente o inválido."""

    def __init__(self, detail: str = "No autenticado"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenError(HTTPException):
    """403 Forbidden - Usuario autenticado pero sin permisos."""

    def __init__(self, detail: str = "Sin permisos"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundError(HTTPException):
    """404 Not Found - Recurso no encontrado."""

    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class MethodNotAllowedError(HTTPException):
    """405 Method Not Allowed - Méthodo no permitido en el endpoint."""

    def __init__(self, detail: str = "Método no permitido"):
        super().__init__(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=detail)


class ConflictError(HTTPException):
    """409 Conflict - Conflicto de estado, p. ej. registro duplicado."""

    def __init__(self, detail: str = "Conflicto"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnprocessableEntityError(HTTPException):
    """422 Unprocessable Entity - Error de validación de datos."""

    def __init__(self, detail: str = "Error de validación de datos"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class InternalServerError(HTTPException):
    """500 Internal Server Error - Excepción no controlada."""

    def __init__(self, detail: str = "Fallo interno"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class BadGatewayError(HTTPException):
    """502 Bad Gateway - Error en un servicio dependiente."""

    def __init__(self, detail: str = "Error entre servicios"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


class ServiceUnavailableError(HTTPException):
    """503 Service Unavailable - Servicio temporalmente no disponible."""

    def __init__(self, detail: str = "Servicio no disponible"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


# Helpers para respuestas de éxito (útiles desde endpoints)
def success_response(data: Any, status_code: int = status.HTTP_200_OK) -> JSONResponse:
    """200 OK - Respuesta genérica con payload JSON."""

    return JSONResponse(status_code=status_code, content={"data": data})


def created_response(data: Optional[Any] = None, location: Optional[str] = None) -> JSONResponse:
    """201 Created - Respuesta al crear un recurso. Se puede incluir Location."""

    headers = {"Location": location} if location else None
    content = {"data": data} if data is not None else None
    # JSONResponse no permite headers=None, así que pasar {} si está vacío
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content or {}, headers=headers or {})


def accepted_response(message: str = "Aceptado para procesamiento asíncrono") -> JSONResponse:
    """202 Accepted - El trabajo fue aceptado para procesamiento asíncrono."""

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": message})


def no_content_response() -> Response:
    """204 No Content - Respuesta sin cuerpo (p. ej. DELETE exitoso)."""

    return Response(status_code=status.HTTP_204_NO_CONTENT)


__all__ = [
    # Errors
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "MethodNotAllowedError",
    "ConflictError",
    "UnprocessableEntityError",
    "InternalServerError",
    "BadGatewayError",
    "ServiceUnavailableError",
    # Success helpers
    "success_response",
    "created_response",
    "accepted_response",
    "no_content_response",
]
