from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class SiniestroInicializarDTO(BaseModel):
    vehiculo_id: str
    vehiculo_marca: str
    vehiculo_modelo: str
    vehiculo_anio: int
    vehiculo_placas: str
    vehiculo_vin: Optional[str] = None
    latitud_siniestro: float
    longitud_siniestro: float
    narracion_texto: Optional[str] = None
    narracion_audio_url: Optional[str] = None
    indicaciones_dano_interno: bool = False
    fecha_siniestro: Optional[datetime] = None

class SiniestroUpdateDTO(BaseModel):
    vehiculo_id: Optional[str] = None
    vehiculo_marca: Optional[str] = None
    vehiculo_modelo: Optional[str] = None
    vehiculo_anio: Optional[int] = None
    vehiculo_placas: Optional[str] = None
    vehiculo_vin: Optional[str] = None
    latitud_siniestro: Optional[float] = None
    longitud_siniestro: Optional[float] = None
    narracion_texto: Optional[str] = None
    narracion_audio_url: Optional[str] = None
    indicaciones_dano_interno: Optional[bool] = None

class SiniestroResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    aseguradora_id: Optional[str] = None
    cliente_id: str
    ajustador_id: Optional[str] = None
    taller_id: Optional[str] = None
    vehiculo_id: Optional[str] = None
    estatus: str
    vehiculo_marca: str
    vehiculo_modelo: str
    vehiculo_anio: int
    vehiculo_placas: str
    vehiculo_vin: Optional[str] = None
    latitud_siniestro: float
    longitud_siniestro: float
    narracion_texto: Optional[str] = None
    narracion_audio_url: Optional[str] = None
    indicaciones_dano_interno: bool
    fecha_siniestro: datetime
    created_at: datetime

class ImagenSiniestroResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    siniestro_id: str
    imagen_url: str
    es_calidad_valida: bool
    metadatos_json: Optional[dict] = None
    created_at: datetime
