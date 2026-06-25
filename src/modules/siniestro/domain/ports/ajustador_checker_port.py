from typing import Protocol

class AjustadorCheckerPort(Protocol):
    def existe_y_activo(self, ajustador_id: str) -> bool: ...
