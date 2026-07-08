from src.core.exceptions import NotFoundError
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel


class ActualizarPerfilAjustador:
    def __init__(self, ajustador_repo, auth_repo):
        self.ajustador_repo = ajustador_repo
        self.auth_repo = auth_repo

    def execute(self, usuario_id: str, nombre: str | None = None, email: str | None = None, telefono: str | None = None) -> AjustadorModel:
        self.auth_repo.update_user_profile(usuario_id, nombre=nombre, email=email, telefono=telefono)
        aj = self.ajustador_repo.get_by_usuario_id(usuario_id)
        if not aj:
            raise NotFoundError("Perfil de ajustador no encontrado.")
        return aj
