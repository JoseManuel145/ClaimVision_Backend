from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PerfilAseguradoraDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre: str
    rfc: str
    dominio_correo: str
    plan_suscripcion: str
    limite_peritajes_mes: int
    peritajes_consumidos_mes: int
    estatus_comercial: str
    contacto_legal_email: str
    created_at: datetime
    updated_at: datetime


class PerfilAseguradoraUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    rfc: Optional[str] = None
    dominio_correo: Optional[str] = None
    contacto_legal_email: Optional[str] = None
    operador_nombre: Optional[str] = None
    operador_email: Optional[str] = None
    operador_telefono: Optional[str] = None
