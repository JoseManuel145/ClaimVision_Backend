from src.modules.catalogo.domain.models import ColorModel
from src.modules.catalogo.domain.ports import ProductoColorPort


class GetColoresByProducto:
    def __init__(self, repo: ProductoColorPort):
        self.repo = repo

    def execute(self, producto_id: str) -> list[ColorModel]:
        return self.repo.get_all_by_producto(producto_id)
