from pydantic import BaseModel
from datetime import date
from typing import Optional


class ConfirmDataRequestDTO(BaseModel):
    numero_poliza: str
    vigencia_poliza: date
    curp_rfc: str
    vehiculo_marca: str
    vehiculo_modelo: str
    vehiculo_anio: int
    vehiculo_placas: str
    vehiculo_vin: Optional[str] = None
    vehiculo_color: Optional[str] = None
