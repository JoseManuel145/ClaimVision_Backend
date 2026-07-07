from typing import List, Tuple

from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort


class ListSiniestrosAseguradora:
    def __init__(self, siniestro_repo: SiniestroRepositoryPort):
        self.siniestro_repo = siniestro_repo

    def execute(
        self,
        aseguradora_id: str,
        offset: int = 0,
        limit: int = 20,
        estatus: str | None = None,
        ajustador_id: str | None = None,
        taller_id: str | None = None,
        q: str | None = None,
    ) -> Tuple[List[SiniestroModel], int]:
        return self.siniestro_repo.list_by_aseguradora(
            aseguradora_id, offset, limit, estatus, ajustador_id, taller_id, q
        )
