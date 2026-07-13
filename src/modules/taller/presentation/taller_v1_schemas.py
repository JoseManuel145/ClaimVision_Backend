from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.modules.siniestro.presentation.siniestros.siniestro_dto import SiniestroResponseDTO
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO


class CotizacionV1DTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    siniestro_id: str
    taller_id: str
    monto_mano_obra: float
    monto_refacciones: float
    monto_total: float
    desglose_pdf_url: str
    estatus: str
    observaciones_tecnicas: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime


class TallerExpedienteDTO(SiniestroResponseDTO):
    peritaje: Optional[PeritajeResponseDTO] = None
    cotizacion: Optional[CotizacionV1DTO] = None


class CrearCotizacionRequest(BaseModel):
    monto_mano_obra: float
    monto_refacciones: float
    monto_total: Optional[float] = None
    observaciones_tecnicas: Optional[str] = None


class EditarCotizacionRequest(BaseModel):
    monto_mano_obra: Optional[float] = None
    monto_refacciones: Optional[float] = None
    monto_total: Optional[float] = None
    desglose_pdf_url: Optional[str] = None
    observaciones_tecnicas: Optional[str] = None


class TallerPerfilUpdateRequest(BaseModel):
    nombre_comercial: Optional[str] = None
    direccion_tecnica: Optional[str] = None
    telefono_contacto: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class TallerPerfilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_comercial: str
    rfc: str
    direccion_tecnica: str
    telefono_contacto: str
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime
