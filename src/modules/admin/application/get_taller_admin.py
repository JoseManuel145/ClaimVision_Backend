from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort
from src.core.exceptions import NotFoundError

class GetTallerAdmin:
    def __init__(self, taller_repo: TallerRepositoryPort):
        self.taller_repo = taller_repo

    def execute(self, taller_id: str) -> dict:
        taller = self.taller_repo.get_by_id(taller_id)
        if not taller:
            raise NotFoundError("Taller no encontrado.")
        return taller
