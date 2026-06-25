from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class DanoAjustadoManualModel:
    id: str
    peritaje_ajustador_id: str
    zona_vehiculo: str
    tipo: str
    severidad: str
    costo_real_reparacion: float
    origen_cambio: str
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

@dataclass
class PeritajeAjustadorModel:
    id: str
    siniestro_id: str
    ajustador_id: str
    costo_definitivo_ajustador: float
    firma_digital_ajustador: str
    observaciones_campo: Optional[str]
    danos: List[DanoAjustadoManualModel]
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
