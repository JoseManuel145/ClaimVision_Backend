from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class DanoAjustadoDTO(BaseModel):
    zona_vehiculo: str
    tipo: str
    severidad: str
    costo_real_reparacion: float
    origen_cambio: str = "AJUSTADOR"

class DanoAjustadoResponseDTO(DanoAjustadoDTO):
    model_config = ConfigDict(from_attributes=True)
    id: str

class PeritajeUpsertRequestDTO(BaseModel):
    costo_definitivo_ajustador: float
    firma_digital_ajustador: str
    observaciones_campo: Optional[str] = None
    danos: List[DanoAjustadoDTO]

class PeritajeResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    siniestro_id: str
    ajustador_id: str
    costo_definitivo_ajustador: float
    firma_digital_ajustador: str
    observaciones_campo: Optional[str]
    danos: List[DanoAjustadoResponseDTO]
    version: int
    created_at: datetime
    updated_at: datetime
