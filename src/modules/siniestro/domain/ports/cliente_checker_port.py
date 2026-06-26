from typing import Protocol, Optional

class ClienteCheckerPort(Protocol):
    def get_perfil_cliente_id_by_usuario(self, usuario_id: str) -> Optional[str]:
        """
        Obtiene el ID del perfil_cliente dado un usuario_id.
        Retorna None si el usuario no ha completado el onboarding.
        """
        ...
