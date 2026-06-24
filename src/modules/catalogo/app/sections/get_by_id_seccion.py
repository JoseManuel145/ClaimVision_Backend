from src.modules.catalogo.domain.models import SeccionModel
from src.modules.catalogo.domain.ports import SeccionPort


class GetByIdSeccion:
    def __init__(self, repo: SeccionPort):
        self.repo = repo

    def execute(self, seccion_id: int) -> SeccionModel | None:
        return self.repo.get_seccion_by_id(seccion_id)