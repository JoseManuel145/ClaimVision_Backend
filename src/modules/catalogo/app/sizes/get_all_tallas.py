from src.modules.catalogo.domain.models import TallaModel
from src.modules.catalogo.domain.ports import TallaPort


class GetAllTallas:
    def __init__(self, repo: TallaPort):
        self.repo = repo

    def execute(self) -> list[TallaModel]:
        return self.repo.get_all()
