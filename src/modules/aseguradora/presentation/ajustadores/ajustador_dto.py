from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AjustadorResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    usuario_id: str
    cedula_profesional: str
    geolocalizacion_actual: Optional[tuple[float, float]]
    activo_para_servicio: bool
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class AjustadorCreateDTO(BaseModel):
    nombre: str
    email: str
    telefono: str
    password_temporal: str
    cedula_profesional: str

class AjustadorUpdateDTO(BaseModel):
    cedula_profesional: Optional[str] = None
    activo_para_servicio: Optional[bool] = None
