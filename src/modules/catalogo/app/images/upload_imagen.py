from src.modules.catalogo.domain.models import ImagenModel
from src.modules.catalogo.domain.ports import ImageStoragePort, ImagePort

class UploadImage:
    def __init__(self, imagen_repo: ImagePort, storage: ImageStoragePort):
        self.imagen_repo = imagen_repo
        self.storage = storage

    def execute(self, imagen_data: bytes, filename: str, orden: int) -> ImagenModel:
        path = f"productos/{filename}"
        self.storage.upload(imagen_data, path)
        imagen = ImagenModel(imagen_id=None, path=path, orden=orden)
        return self.imagen_repo.create(imagen)