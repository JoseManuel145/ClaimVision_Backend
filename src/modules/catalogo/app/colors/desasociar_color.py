from src.modules.catalogo.domain.ports import ProductoColorPort


class DesasociarColor:
    def __init__(self, repo: ProductoColorPort):
        self.repo = repo

    def execute(self, producto_id: str, talla_id: int) -> None:
        return self.repo.remove_from_producto(producto_id, talla_id)
