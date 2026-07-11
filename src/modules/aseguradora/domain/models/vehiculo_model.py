from dataclasses import dataclass
from datetime import datetime

@dataclass
class VehiculoModel:
    id: str
    aseguradora_id: str
    cliente_id: str
    marca: str
    modelo: str
    anio: int
    placas: str
    vin: str | None
    color: str | None
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
