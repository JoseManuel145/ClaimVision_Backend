from src.core.exceptions import NotFoundError, ForbiddenError


class GetPerfilTaller:
    def __init__(self, perfil_taller_repo, taller_repo, auth_repo):
        self.perfil_taller_repo = perfil_taller_repo
        self.taller_repo = taller_repo
        self.auth_repo = auth_repo

    def execute(self, usuario_id: str):
        taller_id = self.perfil_taller_repo.get_taller_id_by_usuario(usuario_id)
        if not taller_id:
            raise ForbiddenError("El usuario no tiene un perfil de taller asignado.")
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado.")
        user_data = self.auth_repo.get_by_id(usuario_id)
        return taller, user_data
