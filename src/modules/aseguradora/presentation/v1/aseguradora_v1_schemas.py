from typing import List, Optional
from pydantic import BaseModel

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO
from src.modules.taller.presentation.v1.taller_v1_schemas import CotizacionV1DTO


class RechazarCotizacionRequest(BaseModel):
    motivo: Optional[str] = None


class SiniestroDetalleAseguradoraDTO(SiniestroResponseDTO):
    imagenes: List[ImagenSiniestroResponseDTO] = []
    peritaje: Optional[PeritajeResponseDTO] = None
    cotizacion: Optional[CotizacionV1DTO] = None
    # Sugerencia IA (§7) — la poblará el motor en P2.
    peritaje_ia: Optional[dict] = None
