from src.modules.catalogo.domain.ports import ProductImagePort, ImageStoragePort, ImagePort

class DeleteImagesByProduct:
    def __init__(
        self,
        imagen_repo: ImagePort,
        producto_imagen_repo: ProductImagePort,
        storage: ImageStoragePort
    ):
        self.imagen_repo = imagen_repo
        self.producto_imagen_repo = producto_imagen_repo
        self.storage = storage

    def execute(self, producto_id: str) -> None:
        relaciones = self.producto_imagen_repo.get_by_producto(producto_id)
        for rel in relaciones:
            imagen = self.imagen_repo.get_by_id(rel.imagen_id)
            if imagen:
                self.storage.delete(imagen.path)
                self.imagen_repo.delete(imagen.imagen_id)
        self.producto_imagen_repo.delete_by_producto(producto_id)