from src.modules.catalogo.domain.ports import ProductImagePort
from src.modules.catalogo.domain.models import ProductoImagenModel
from src.modules.catalogo.presentation.images.images_dto import ProductoImagenCreateDTO

class AsociarImageToProduct:
    def __init__(self, producto_imagen_repo: ProductImagePort):
        self.producto_imagen_repo = producto_imagen_repo

    def execute(self, dto: ProductoImagenCreateDTO) -> ProductoImagenModel:
        producto_imagen = ProductoImagenModel(
            producto_imagen_id=None,
            producto_id=dto.producto_id,
            imagen_id=dto.imagen_id,
            es_principal=dto.es_principal
        )
        return self.producto_imagen_repo.create(producto_imagen)