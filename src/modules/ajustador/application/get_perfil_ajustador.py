from src.core.exceptions import NotFoundError
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel


class GetPerfilAjustador:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, usuario_id: str) -> AjustadorModel:
        aj = self.repo.get_by_usuario_id(usuario_id)
        if not aj:
            raise NotFoundError("Perfil de ajustador no encontrado.")
        return aj
