from typing import List, Tuple
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.cliente_checker_port import ClienteCheckerPort
from src.core.exceptions import BusinessRuleError


class ListSiniestrosCliente:
    """Lista los siniestros del cliente autenticado (filtrados por su perfil)."""

    def __init__(self, repo: SiniestroRepositoryPort, cliente_checker: ClienteCheckerPort):
        self.repo = repo
        self.cliente_checker = cliente_checker

    def execute(
        self, usuario_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None
    ) -> Tuple[List[SiniestroModel], int]:
        perfil_cliente_id = self.cliente_checker.get_perfil_cliente_id_by_usuario(usuario_id)
        if not perfil_cliente_id:
            raise BusinessRuleError("El usuario no tiene un perfil de cliente (onboarding incompleto).")
        return self.repo.list_by_cliente(perfil_cliente_id, offset, limit, estatus)
