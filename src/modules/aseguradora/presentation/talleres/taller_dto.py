from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime
from typing import Optional

class TallerResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_comercial: str
    rfc: str
    direccion_tecnica: str
    telefono_contacto: str
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class OperadorTallerRequestDTO(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)
    puesto: str = Field(default="Operador")

class TallerCreateDTO(BaseModel):
    nombre_comercial: str = Field(..., min_length=1, max_length=200)
    rfc: str = Field(..., min_length=12, max_length=13, pattern=r'^[A-ZÑ&]{3,4}\d{6}[A-Za-z\d]{3}$')
    direccion_tecnica: str = Field(..., min_length=5, max_length=500)
    telefono_contacto: str = Field(..., min_length=10, max_length=15)

class TallerUpdateDTO(BaseModel):
    nombre_comercial: Optional[str] = None
    direccion_tecnica: Optional[str] = None
    telefono_contacto: Optional[str] = None
