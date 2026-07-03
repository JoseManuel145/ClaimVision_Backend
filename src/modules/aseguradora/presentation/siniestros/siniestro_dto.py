from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO
from src.modules.taller.presentation.taller_v1_schemas import CotizacionV1DTO


class AsignarAjustadorDTO(BaseModel):
    ajustador_id: str


class EnviarTallerDTO(BaseModel):
    taller_id: str


class RechazarCotizacionRequest(BaseModel):
    motivo: Optional[str] = None


class SiniestroDetalleAseguradoraDTO(SiniestroResponseDTO):
    imagenes: List[ImagenSiniestroResponseDTO] = []
    peritaje: Optional[PeritajeResponseDTO] = None
    cotizacion: Optional[CotizacionV1DTO] = None
    peritaje_ia: Optional[dict] = None
