import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


def validate_password_strength(v: str) -> str:
    if len(v) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if not re.search(r"[A-Z]", v):
        raise ValueError("La contraseña debe contener al menos una mayúscula")
    if not re.search(r"[a-z]", v):
        raise ValueError("La contraseña debe contener al menos una minúscula")
    if not re.search(r"\d", v):
        raise ValueError("La contraseña debe contener al menos un número")
    return v


# para el MVP
class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)

class LoginRequestDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    usuario_id: str
    nombre: str
    email: EmailStr
    fecha_creacion: datetime

    telefono: str | None = None
    rol: str | None = "cliente"
    estado: str = "Activo"
    aseguradora_id: str | None = None
    fecha_eliminacion: datetime | None = None

class LoginResponseDTO(BaseModel):
    token: str
    usuario_id: str
    email: str
    rol: str
    aseguradora_id: str | None

class ConsentRequestDTO(BaseModel):
    aviso_privacidad: bool
    biometria: bool
    transferencia_talleres: bool


class RecoveryRequestDTO(BaseModel):
    email: EmailStr


class RecoveryVerifyDTO(BaseModel):
    usuario_id: str
    code: str


class RecoveryResetDTO(BaseModel):
    usuario_id: str
    code: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)


class ChangePasswordWithCodeRequest(BaseModel):
    code: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def check_password(cls, v: str) -> str:
        return validate_password_strength(v)


class DeviceTokenRequestDTO(BaseModel):
    token: str
