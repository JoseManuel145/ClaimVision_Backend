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
    nombre_comercial: str
    rfc: str
    direccion_tecnica: str
    telefono_contacto: str

class TallerUpdateDTO(BaseModel):
    nombre_comercial: Optional[str] = None
    direccion_tecnica: Optional[str] = None
    telefono_contacto: Optional[str] = None
