from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class AseguradoraRequestDTO(BaseModel):
    nombre: str
    rfc: str
    dominio_correo: str
    plan_suscripcion: str
    contacto_legal_email: str

class AseguradoraResponseDTO(BaseModel):
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
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class UpdateSuscripcionDTO(BaseModel):
    nuevo_plan: str
    limite_peritajes_mes: int

class AuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str | None
    usuario_id: str | None
    aseguradora_id: str | None
    evento_modulo: str | None
    accion_realizada: str | None
    direccion_ip: str | None
    user_agent: str | None
    metadata_context: Dict[str, Any] | None
    created_at: datetime
