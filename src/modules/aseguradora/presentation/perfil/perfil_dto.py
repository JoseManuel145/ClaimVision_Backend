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
