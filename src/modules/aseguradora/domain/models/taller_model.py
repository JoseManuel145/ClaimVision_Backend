from dataclasses import dataclass
from datetime import datetime

@dataclass
class TallerModel:
    id: str
    nombre_comercial: str
    rfc: str
    direccion_tecnica: str
    telefono_contacto: str
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
