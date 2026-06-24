from src.modules.aseguradora.domain.models.taller_model import TallerModel
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort
from src.core.exceptions import NotFoundError

class GetTaller:
    def __init__(self, repo: TallerRepositoryPort):
        self.repo = repo

    def execute(self, id: str) -> TallerModel:
        taller = self.repo.get_by_id(id)
        if not taller:
            raise NotFoundError("Taller no encontrado")
        return taller
