from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CotizacionTallerModel:
    id: str
    siniestro_id: str
    taller_id: str
    monto_mano_obra: float
    monto_refacciones: float
    monto_total: float
    desglose_pdf_url: str
    estatus: str
    observaciones_tecnicas: Optional[str]
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
