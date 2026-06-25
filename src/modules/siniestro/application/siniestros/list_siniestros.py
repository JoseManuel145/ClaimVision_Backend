from typing import List, Tuple
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort

class ListSiniestros:
    def __init__(self, repo: SiniestroRepositoryPort):
        self.repo = repo

    def execute(self, aseguradora_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None) -> Tuple[List[SiniestroModel], int]:
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit, estatus)
