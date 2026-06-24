from typing import List, Tuple
from src.modules.aseguradora.domain.models.taller_model import TallerModel
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort

class ListTalleres:
    def __init__(self, repo: TallerRepositoryPort):
        self.repo = repo

    def execute(self, aseguradora_id: str, offset: int = 0, limit: int = 20) -> Tuple[List[TallerModel], int]:
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit)
