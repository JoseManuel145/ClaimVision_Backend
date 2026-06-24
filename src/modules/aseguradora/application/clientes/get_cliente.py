from src.modules.aseguradora.domain.models.cliente_model import ClienteModel
from src.modules.aseguradora.domain.ports.cliente_repository_port import ClienteRepositoryPort
from src.core.exceptions import NotFoundError

class GetCliente:
    def __init__(self, repo: ClienteRepositoryPort):
        self.repo = repo

    def execute(self, id: str) -> ClienteModel:
        cliente = self.repo.get_by_id(id)
        if not cliente:
            raise NotFoundError("Cliente no encontrado")
        return cliente
