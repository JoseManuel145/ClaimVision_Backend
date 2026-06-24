from src.modules.catalogo.domain.models import CategoriaModel
from src.modules.catalogo.domain.ports.categoria_port import CategoriaPort
from src.modules.catalogo.presentation.category.categoria_dto import CategoriaUpdate

class UpdateCategory:
    def __init__(self, repo: CategoriaPort):
        self.repo = repo

    def execute(self, categoria_id: int, dto: CategoriaUpdate) -> CategoriaModel | None:
        current = self.repo.get_by_id(categoria_id)
        if not current:
            raise ValueError(f"Categoria {categoria_id} not found")

        current.nombre = dto.nombre
        current.seccion_id = dto.seccion_id

        return self.repo.update(categoria_id, current)
