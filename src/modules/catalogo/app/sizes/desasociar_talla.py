from src.modules.catalogo.domain.ports.talla_port import ProductoTallaPort


class DesasociarTalla:
    def __init__(self, repo: ProductoTallaPort):
        self.repo = repo

    def execute(self, producto_id: str, talla_id: int) -> None:
        return self.repo.remove_from_producto(producto_id, talla_id)
