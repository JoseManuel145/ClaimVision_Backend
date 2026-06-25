from typing import Protocol

class TallerCheckerPort(Protocol):
    def existe(self, taller_id: str) -> bool: ...
