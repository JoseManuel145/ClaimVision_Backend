from src.modules.catalogo.domain.ports import ImageStoragePort, ImagePort

class DeleteImage:
    def __init__(self, imagen_repo: ImagePort, storage: ImageStoragePort):
        self.imagen_repo = imagen_repo
        self.storage = storage

    def execute(self, imagen_id: int) -> None:
        imagen = self.imagen_repo.get_by_id(imagen_id)
        if not imagen:
            return
        self.storage.delete(imagen.path)
        self.imagen_repo.delete(imagen_id)