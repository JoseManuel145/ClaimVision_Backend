from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort
from src.core.exceptions import NotFoundError

class DeleteTaller:
    def __init__(self, repo: TallerRepositoryPort):
        self.repo = repo

    def execute(self, id: str, aseguradora_id: str) -> None:
        taller = self.repo.get_by_id(id)
        if not taller:
            raise NotFoundError("Taller no encontrado")
        
        self.repo.desvincular_taller_aseguradora(id, aseguradora_id)
