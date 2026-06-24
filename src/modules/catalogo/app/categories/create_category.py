from src.modules.catalogo.domain.models import CategoriaModel
from src.modules.catalogo.domain.ports.categoria_port import CategoriaPort
from src.modules.catalogo.presentation.category.categoria_dto import CategoriaCreate


class CreateCategory:
    def __init__(self, repo: CategoriaPort):
        self.repo = repo

    def execute(self, dto: CategoriaCreate) -> CategoriaModel:
        model = CategoriaModel(
            categoria_id=None,
            nombre=dto.nombre,
            seccion_id=dto.seccion_id,
        )
        return self.repo.create(model)
