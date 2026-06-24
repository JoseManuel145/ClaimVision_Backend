from pydantic import BaseModel, ConfigDict
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

class TallerCreateDTO(BaseModel):
    nombre_comercial: str
    rfc: str
    direccion_tecnica: str
    telefono_contacto: str

class TallerUpdateDTO(BaseModel):
    nombre_comercial: Optional[str] = None
    direccion_tecnica: Optional[str] = None
    telefono_contacto: Optional[str] = None
