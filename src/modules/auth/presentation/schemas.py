from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

# para el MVP
class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str

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
