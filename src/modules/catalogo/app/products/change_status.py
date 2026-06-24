from src.modules.catalogo.domain.models import ProductoModel
from src.modules.catalogo.domain.ports import ProductoPort


class ChangeStatus:
    def __init__(self, repo: ProductoPort):
        self.repo = repo

    def execute(self, producto_id: str, status: bool) -> ProductoModel:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise ValueError(f"Producto {producto_id} no existe")
        producto.esta_activo = status
        return self.repo.update_producto(producto_id, producto)