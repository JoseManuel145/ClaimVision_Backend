from pydantic import BaseModel
from datetime import date

class ConfirmDataRequestDTO(BaseModel):
    numero_poliza: str
    vigencia_poliza: date
    curp_rfc: str
