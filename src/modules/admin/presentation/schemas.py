from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Dict, Any, List, Generic, TypeVar
import math

MAX_PAGE_SIZE = 100

T = TypeVar("T")

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

class UpdateAseguradoraDTO(BaseModel):
    nombre: Optional[str] = None
    rfc: Optional[str] = None
    dominio_correo: Optional[str] = None
    contacto_legal_email: Optional[str] = None

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

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    @classmethod
    def build(cls, items: List[T], total: int, page: int, page_size: int) -> "PaginatedResponse[T]":
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=math.ceil(total / page_size) if page_size > 0 else 0,
        )

