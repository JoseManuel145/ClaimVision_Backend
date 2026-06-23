from datetime import datetime
from dataclasses import dataclass
from src.shared.domain.models import Rol, EstadoUsuario

@dataclass
class AuthUser:
    usuario_id: str
    nombre: str
    email: str
    rol: str
    fecha_creacion: datetime
    is_authenticated: bool = False
    estado: str = EstadoUsuario.ACTIVO.value
    aseguradora_id: str | None = None

    # Actualizados a la sintaxis moderna | None
    password: str | None = None
    telefono: str | None = None
    google_id: str | None = None
    fecha_eliminacion: datetime | None = None

@dataclass
class AuthenticatedUser:
    usuario_id: str
    email: str
    rol: str
    aseguradora_id: str | None = None

@dataclass
class TokenPayload:
    usuario_id: str
    email: str
    rol: str
    aseguradora_id: str | None
    exp: datetime

@dataclass
class TokenResult:
    token: str
    usuario_id: str
    email: str
    rol: str
    aseguradora_id: str | None

@dataclass
class RecoveryCode:
    id: int | None
    usuario_id: str
    code: str
    expires_at: datetime

    def is_expired(self, now: datetime) -> bool:
        return now > self.expires_at