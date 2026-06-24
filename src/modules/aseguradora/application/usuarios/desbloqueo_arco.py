from src.modules.aseguradora.domain.ports.usuario_repository_port import UsuarioRepositoryPort
from src.core.exceptions import NotFoundError, BusinessRuleError

class DesbloqueoArcoAseguradora:
    def __init__(self, user_repo: UsuarioRepositoryPort):
        self.user_repo = user_repo

    def execute(self, aseguradora_id: str, usuario_id: str) -> None:
        user = self.user_repo.get_by_id(usuario_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
            
        if user.get("aseguradora_id") != aseguradora_id:
            raise BusinessRuleError("No puedes aplicar desbloqueo ARCO a un usuario de otra aseguradora")
            
        self.user_repo.desbloquear_por_arco(usuario_id)
