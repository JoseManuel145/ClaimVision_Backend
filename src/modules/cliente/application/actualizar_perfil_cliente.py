from src.modules.cliente.domain.models import ClienteProfile


class ActualizarPerfilCliente:
    def __init__(self, cliente_repo, auth_repo):
        self.cliente_repo = cliente_repo
        self.auth_repo = auth_repo

    def execute(self, usuario_id: str, nombre: str | None = None, email: str | None = None, telefono: str | None = None) -> ClienteProfile:
        self.auth_repo.update_user_profile(usuario_id, nombre=nombre, email=email, telefono=telefono)
        perfil = self.cliente_repo.get_by_usuario_id(usuario_id)
        return perfil
