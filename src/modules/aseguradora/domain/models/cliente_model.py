from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class ClienteModel:
    id: str
    usuario_id: str
    numero_poliza: str
    vigencia_poliza: date
    curp_rfc_cifrado: str
    consentimiento_aviso_privacidad: bool
    consentimiento_biometria: bool
    autoriza_transferencia_talleres: bool
    fecha_consentimiento: datetime | None
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    nombre: str | None = None
    email: str | None = None
    telefono: str | None = None
