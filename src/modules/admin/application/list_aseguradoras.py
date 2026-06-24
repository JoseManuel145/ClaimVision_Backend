from typing import List, Tuple
from src.modules.admin.domain.models import AseguradoraTenant
from src.modules.admin.domain.ports import AseguradoraRepositoryPort

class ListAseguradoras:
    def __init__(self, repo: AseguradoraRepositoryPort):
        self.repo = repo

    def execute(self, offset: int = 0, limit: int = 20, include_deleted: bool = False) -> Tuple[List[AseguradoraTenant], int]:
        return self.repo.list_all(offset=offset, limit=limit, include_deleted=include_deleted)

