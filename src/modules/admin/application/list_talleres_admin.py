from typing import List, Tuple
from src.modules.aseguradora.domain.models.taller_model import TallerModel
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort

class ListTalleresAdmin:
    def __init__(self, taller_repo: TallerRepositoryPort):
        self.taller_repo = taller_repo

    def execute(self, offset: int = 0, limit: int = 20) -> Tuple[List[TallerModel], int]:
        return self.taller_repo.list_all(offset=offset, limit=limit)
