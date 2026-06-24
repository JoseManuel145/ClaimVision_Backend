from src.modules.catalogo.domain.ports import ProductImagePort, ImagePort
from src.modules.catalogo.domain.models import ImagenModel

class GetImagesByProduct:
    def __init__(self, imagen_repo: ImagePort, producto_imagen_repo: ProductImagePort):
        self.imagen_repo = imagen_repo
        self.producto_imagen_repo = producto_imagen_repo

    def execute(self, producto_id: str) -> list[ImagenModel]:
        relaciones = self.producto_imagen_repo.get_by_producto(producto_id)
        imagenes: list[ImagenModel] = []
        for rel in relaciones:
            imagen = self.imagen_repo.get_by_id(rel.imagen_id)
            if imagen:
                imagenes.append(imagen)
        return imagenes