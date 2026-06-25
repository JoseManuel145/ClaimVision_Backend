from dataclasses import dataclass
from datetime import datetime
from src.shared.domain.models import EstatusSiniestro

@dataclass
class SiniestroModel:
    id: str
    aseguradora_id: str
    cliente_id: str
    ajustador_id: str | None
    taller_id: str | None
    estatus: str
    vehiculo_marca: str
    vehiculo_modelo: str
    vehiculo_anio: int
    vehiculo_placas: str
    vehiculo_vin: str | None
    latitud_siniestro: float
    longitud_siniestro: float
    narracion_texto: str | None
    narracion_audio_url: str | None
    indicaciones_dano_interno: bool
    fecha_siniestro: datetime
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
