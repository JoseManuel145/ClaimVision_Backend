from dataclasses import dataclass
from datetime import datetime

@dataclass
class ImagenSiniestroModel:
    id: str
    siniestro_id: str
    imagen_url: str
    es_calidad_valida: bool
    metadatos_json: dict | None
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
