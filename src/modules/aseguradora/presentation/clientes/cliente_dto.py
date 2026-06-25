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

class ClienteCreateDTO(BaseModel):
    nombre: str
    email: str
    telefono: str
    password_temporal: str
