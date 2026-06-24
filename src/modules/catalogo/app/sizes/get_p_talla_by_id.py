from src.modules.catalogo.domain.models import ProductoTallaModel
from src.modules.catalogo.domain.ports.talla_port import ProductoTallaPort


class GetPTallaById:
    def __init__(self, repo: ProductoTallaPort):
        self.repo = repo

    def execute(self, p_talla_id: int) -> ProductoTallaModel | None:
        p_talla = self.repo.get_by_id(p_talla_id)
        if not p_talla:
            raise ValueError(f"No existe {p_talla_id}")
        return p_talla
