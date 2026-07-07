from typing import List, Tuple

from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.modules.ajustador.application._helpers import resolver_ajustador_id


class ListMisAsignaciones:
    def __init__(self, ajustador_repo: AjustadorRepositoryPort, siniestro_repo: SiniestroRepositoryPort):
        self.ajustador_repo = ajustador_repo
        self.siniestro_repo = siniestro_repo

    def execute(
        self, usuario_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None
    ) -> Tuple[List[SiniestroModel], int]:
        ajustador_id = resolver_ajustador_id(self.ajustador_repo, usuario_id)
        return self.siniestro_repo.list_by_ajustador(ajustador_id, offset, limit, estatus)
