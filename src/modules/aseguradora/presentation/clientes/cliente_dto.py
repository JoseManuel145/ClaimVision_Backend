from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional

class ClienteResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    usuario_id: str
    numero_poliza: str
    vigencia_poliza: date
    # No se expone curp_rfc_cifrado
    consentimiento_aviso_privacidad: bool
    consentimiento_biometria: bool
    autoriza_transferencia_talleres: bool
    fecha_consentimiento: Optional[datetime]
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None

class ClienteCreateDTO(BaseModel):
    nombre: str
    email: str
    telefono: str
    password_temporal: str


class ClienteUpdateDTO(BaseModel):
    nombre: str | None = None
    email: str | None = None
    telefono: str | None = None
    numero_poliza: str | None = None
    vigencia_poliza: date | None = None
