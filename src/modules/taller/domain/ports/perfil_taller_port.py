from typing import Protocol, Optional

class PerfilTallerRepositoryPort(Protocol):
    def get_taller_id_by_usuario(self, usuario_id: str) -> Optional[str]: ...
