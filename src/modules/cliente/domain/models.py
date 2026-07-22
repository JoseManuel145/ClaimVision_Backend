from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class ClienteProfile:
    id: str | None
    usuario_id: str
    numero_poliza: str
    vigencia_poliza: date
    curp_rfc_cifrado: str
    consentimiento_aviso_privacidad: bool
    consentimiento_biometria: bool
    autoriza_transferencia_talleres: bool
    fecha_consentimiento: datetime | None
    fecha_creacion: datetime | None = None

@dataclass
class ClienteDocumento:
    id: str | None
    usuario_id: str
    identificacion_url: str | None
    identificacion_tipo: str | None
    identificacion_subido_en: datetime | None
    poliza_url: str | None
    poliza_tipo: str | None
    poliza_subido_en: datetime | None
    created_at: datetime | None = None
    updated_at: datetime | None = None

