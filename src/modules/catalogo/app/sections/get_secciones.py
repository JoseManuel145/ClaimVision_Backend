from src.modules.catalogo.domain.models import SeccionModel
from src.modules.catalogo.domain.ports import SeccionPort


class GetSecciones:
    def __init__(self, repo: SeccionPort):
        self.repo = repo

    def execute(self) -> list[SeccionModel]:
        return self.repo.get_secciones()