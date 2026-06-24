from dataclasses import dataclass
from datetime import datetime

@dataclass
class AjustadorProfile:
    id: str | None
    usuario_id: str
    cedula_ajustador: str
    fecha_creacion: datetime | None = None
