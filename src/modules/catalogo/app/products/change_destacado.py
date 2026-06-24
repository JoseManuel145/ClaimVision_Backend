from src.modules.catalogo.domain.models import ProductoModel
from src.modules.catalogo.domain.ports import ProductoPort


class ChangeDestacado:
    def __init__(self, repo: ProductoPort):
        self.repo = repo

    def execute(self, producto_id: str, destacado: bool) -> ProductoModel:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise ValueError(f"Producto {producto_id} no existe")
        producto.esta_destacado = destacado
        return self.repo.update_producto(producto_id, producto)