from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.siniestro.presentation.peritaje.peritaje_dto import (
    PeritajeResponseDTO,
    DanoAjustadoDTO,
)


class SiniestroDetalleAjustadorDTO(SiniestroResponseDTO):
    imagenes: List[ImagenSiniestroResponseDTO] = []
    peritaje: Optional[PeritajeResponseDTO] = None
    # Sugerencia IA (§7) — aún no implementada; el motor la poblará en P2.
    peritaje_ia: Optional[dict] = None


class EditarPeritajeRequest(BaseModel):
    costo_definitivo_ajustador: Optional[float] = None
    firma_digital_ajustador: Optional[str] = None
    observaciones_campo: Optional[str] = None


class AjustadorPerfilUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class DisponibilidadRequest(BaseModel):
    activo_para_servicio: bool


class GeolocalizacionRequest(BaseModel):
    latitud: float
    longitud: float


class AjustadorPerfilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    usuario_id: str
    cedula_profesional: str
    activo_para_servicio: bool
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    version: int


# Reexport para uso en las rutas
DanoRequest = DanoAjustadoDTO
