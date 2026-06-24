from dataclasses import dataclass
from datetime import datetime

@dataclass
class AjustadorModel:
    id: str
    usuario_id: str
    cedula_profesional: str
    geolocalizacion_actual: tuple[float, float] | None
    activo_para_servicio: bool
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
