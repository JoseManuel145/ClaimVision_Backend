from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.core.exceptions import NotFoundError

class GetAjustador:
    def __init__(self, repo: AjustadorRepositoryPort):
        self.repo = repo

    def execute(self, id: str) -> AjustadorModel:
        ajustador = self.repo.get_by_id(id)
        if not ajustador:
            raise NotFoundError("Ajustador no encontrado")
        return ajustador
