import uuid
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from src.core.exceptions import BusinessRuleError

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

    @field_validator("taller_id")
    @classmethod
    def validar_uuid(cls, v: str) -> str:
        try:
            uuid.UUID(v)
        except (ValueError, AttributeError):
            raise BusinessRuleError(f"El ID del taller '{v}' no es un UUID válido.")
        return v


class RechazarCotizacionRequest(BaseModel):
    motivo: Optional[str] = None


class SiniestroDetalleAseguradoraDTO(SiniestroResponseDTO):
    imagenes: List[ImagenSiniestroResponseDTO] = []
    peritaje: Optional[PeritajeResponseDTO] = None
    cotizacion: Optional[CotizacionV1DTO] = None
    peritaje_ia: Optional[dict] = None
    cliente_nombre: Optional[str] = None
    ajustador_nombre: Optional[str] = None
    taller_nombre: Optional[str] = None
