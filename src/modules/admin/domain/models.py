from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

@dataclass
class AseguradoraTenant:
    id: str | None
    nombre: str
    rfc: str
    dominio_correo: str
    plan_suscripcion: str
    limite_peritajes_mes: int
    peritajes_consumidos_mes: int
    estatus_comercial: str
    contacto_legal_email: str
    version: int = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

@dataclass
class AuditLog:
    id: str | None
    usuario_id: str | None
    usuario_rol: str | None
    usuario_nombre: str | None
    usuario_email: str | None
    aseguradora_id: str | None
    evento_modulo: str | None
    accion_realizada: str | None
    direccion_ip: str | None
    user_agent: str | None
    metadata_context: Dict[str, Any] | None
    created_at: datetime
