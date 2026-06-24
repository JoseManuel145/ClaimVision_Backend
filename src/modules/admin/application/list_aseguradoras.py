from typing import List
from src.modules.admin.domain.models import AseguradoraTenant
from src.modules.admin.domain.ports import AseguradoraRepositoryPort

class ListAseguradoras:
    def __init__(self, repo: AseguradoraRepositoryPort):
        self.repo = repo

    def execute(self) -> List[AseguradoraTenant]:
        return self.repo.list_all()
