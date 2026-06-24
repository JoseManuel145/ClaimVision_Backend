from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SiniestroResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    aseguradora_id: str
    cliente_id: str
    ajustador_id: Optional[str]
    taller_id: Optional[str]
    estatus: str
    vehiculo_marca: str
    vehiculo_modelo: str
    vehiculo_anio: int
    vehiculo_placas: str
    vehiculo_vin: Optional[str]
    latitud_siniestro: float
    longitud_siniestro: float
    narracion_texto: Optional[str]
    narracion_audio_url: Optional[str]
    indicaciones_dano_interno: bool
    fecha_siniestro: datetime
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

class AsignarAjustadorDTO(BaseModel):
    ajustador_id: str

class EnviarTallerDTO(BaseModel):
    taller_id: str
