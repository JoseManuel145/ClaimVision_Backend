from src.modules.cliente.domain.models import ClienteProfile
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.core.exceptions import NotFoundError


class GetPerfilCliente:
    """Devuelve el perfil de cliente (`perfiles_clientes`) del usuario autenticado."""

    def __init__(self, repo: ClienteRepositoryPort):
        self.repo = repo

    def execute(self, usuario_id: str) -> ClienteProfile:
        perfil = self.repo.get_by_usuario_id(usuario_id)
        if not perfil:
            raise NotFoundError("Perfil de cliente no inicializado. Complete su onboarding.")
        return perfil
