from typing import List, Tuple
from src.modules.aseguradora.domain.models.cliente_model import ClienteModel
from src.modules.aseguradora.domain.ports.cliente_repository_port import ClienteRepositoryPort

class ListClientes:
    def __init__(self, repo: ClienteRepositoryPort):
        self.repo = repo

    def execute(self, aseguradora_id: str, offset: int = 0, limit: int = 20) -> Tuple[List[ClienteModel], int]:
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit)
