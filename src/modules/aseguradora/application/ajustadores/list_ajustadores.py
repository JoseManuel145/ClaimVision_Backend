from typing import List, Tuple
from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort

class ListAjustadores:
    def __init__(self, repo: AjustadorRepositoryPort):
        self.repo = repo

    def execute(self, aseguradora_id: str, offset: int = 0, limit: int = 20, activo_para_servicio: bool | None = None) -> Tuple[List[AjustadorModel], int]:
        return self.repo.list_by_aseguradora(aseguradora_id, offset, limit, activo_para_servicio)
