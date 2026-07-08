from pydantic import BaseModel, ConfigDict, EmailStr
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

class OperadorAseguradoraRequestDTO(BaseModel):
    nombre: str
    email: EmailStr
    password: str

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

# ── Usuarios ─────────────────────────────────────────────────────────────

class CreateUsuarioRequestDTO(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str
    aseguradora_id: Optional[str] = None
    telefono: Optional[str] = None

class UpdateUsuarioRequestDTO(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    aseguradora_id: Optional[str] = None
    telefono: Optional[str] = None

class UsuarioResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    nombre_completo_cifrado: str
    telefono_cifrado: Optional[str] = None
    rol: str
    estatus_arco: str
    aseguradora_id: Optional[str] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None

# ── Talleres (admin global) ──────────────────────────────────────────────

class TallerAdminResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_comercial: str
    rfc: str
    direccion_tecnica: str
    telefono_contacto: str
    aseguradoras_vinculadas: List[str] = []
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# ── Dashboard ────────────────────────────────────────────────────────────

class EstatusCountDTO(BaseModel):
    estatus: str
    count: int

class SiniestrosPorMesDTO(BaseModel):
    mes: str
    count: int

class DashboardResumenDTO(BaseModel):
    total_siniestros: int
    siniestros_por_estatus: List[EstatusCountDTO] = []
    siniestros_por_mes: List[SiniestrosPorMesDTO] = []
    usuarios_activos: int
    total_aseguradoras: int
    aseguradoras_activas: int
    total_talleres: int
    talleres_pendientes: int

# ── Purge ───────────────────────────────────────────────────────────────

class PurgeAseguradoraResponse(BaseModel):
    purged: bool
    aseguradora_id: str
    aseguradora_nombre: str
    deleted: Dict[str, int]


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

