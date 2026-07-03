from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)


class RegistrarImagenRequest(BaseModel):
    imagen_url: str
    metadatos_json: Optional[dict] = None


class ConsentimientosRequest(BaseModel):
    consentimiento_aviso_privacidad: bool
    consentimiento_biometria: bool
    autoriza_transferencia_talleres: bool


class PerfilClienteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    usuario_id: str
    numero_poliza: str
    vigencia_poliza: date
    consentimiento_aviso_privacidad: bool
    consentimiento_biometria: bool
    autoriza_transferencia_talleres: bool
    fecha_consentimiento: Optional[datetime] = None


class TimelineItemDTO(BaseModel):
    estatus: str
    alcanzado: bool
    actual: bool


class SiniestroDetalleClienteDTO(SiniestroResponseDTO):
    imagenes: List[ImagenSiniestroResponseDTO] = []
    timeline: List[TimelineItemDTO] = []
