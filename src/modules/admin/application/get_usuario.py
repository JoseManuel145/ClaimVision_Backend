from src.modules.admin.domain.ports import AdminUserRepositoryPort
from src.core.exceptions import NotFoundError

class GetUsuario:
    def __init__(self, user_repo: AdminUserRepositoryPort):
        self.user_repo = user_repo

    def execute(self, usuario_id: str) -> dict:
        user = self.user_repo.get_by_id(usuario_id)
        if not user:
            raise NotFoundError("Usuario no encontrado.")
        return user
