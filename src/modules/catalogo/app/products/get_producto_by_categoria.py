from src.modules.catalogo.domain.models import ProductoModel
from src.modules.catalogo.domain.ports import ProductoPort
from src.modules.catalogo.app.images.get_images import GetImages


class GetProductoByCategoria:
    def __init__(self, repo: ProductoPort, uc: GetImages):
        self.repo = repo
        self.img_uc = uc

    def execute(self, categoria_id: int) -> list[ProductoModel]:
        productos = self.repo.get_by_categoria(categoria_id)

        for p in productos:
            p.imagenes = self.img_uc.execute(p.producto_id)
        return productos