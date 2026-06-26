from typing import Optional
from src.modules.siniestro.domain.ports.cliente_checker_port import ClienteCheckerPort
from src.modules.cliente.domain.ports import ClienteRepositoryPort

class ClienteCheckerAdapter(ClienteCheckerPort):
    def __init__(self, repo: ClienteRepositoryPort):
        self.repo = repo

    def get_perfil_cliente_id_by_usuario(self, usuario_id: str) -> Optional[str]:
        perfil = self.repo.get_by_usuario_id(usuario_id)
        if not perfil:
            return None
        return str(perfil.id)
