from src.modules.siniestro.domain.ports.taller_checker_port import TallerCheckerPort
from src.modules.aseguradora.domain.ports.taller_repository_port import TallerRepositoryPort

class TallerCheckerAdapter(TallerCheckerPort):
    def __init__(self, repo: TallerRepositoryPort):
        self.repo = repo

    def existe(self, taller_id: str) -> bool:
        taller = self.repo.get_by_id(taller_id)
        return taller is not None
