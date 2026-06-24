from src.modules.catalogo.domain.models import CategoriaModel
from src.modules.catalogo.domain.ports.categoria_port import CategoriaPort

class GetAllCategories:
    def __init__(self, repo: CategoriaPort):
        self.repo = repo

    def execute(self) -> list[CategoriaModel]:
        return self.repo.get_all()