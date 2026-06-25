from src.modules.siniestro.domain.ports.ajustador_checker_port import AjustadorCheckerPort
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort

class AjustadorCheckerAdapter(AjustadorCheckerPort):
    def __init__(self, repo: AjustadorRepositoryPort):
        self.repo = repo

    def existe_y_activo(self, ajustador_id: str) -> bool:
        ajustador = self.repo.get_by_id(ajustador_id)
        if not ajustador:
            return False
        return ajustador.activo_para_servicio
