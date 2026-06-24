from src.modules.catalogo.domain.models import TallaModel
from src.modules.catalogo.domain.ports.talla_port import ProductoTallaPort


class GetTallasByProducto:
    def __init__(self, repo: ProductoTallaPort):
        self.repo = repo

    def execute(self, producto_id: str) -> list[TallaModel]:
        return self.repo.get_all_by_producto(producto_id)  # el repositorio hace el join y retorna las coincidencias
