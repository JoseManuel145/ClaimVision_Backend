import uuid
from datetime import datetime
from src.modules.siniestro.domain.models.imagen_siniestro_model import ImagenSiniestroModel
from src.modules.siniestro.domain.ports.imagen_siniestro_repository_port import ImagenSiniestroRepositoryPort
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.storage_port import StoragePort
from src.core.exceptions import NotFoundError

class SubirImagenSiniestro:
    def __init__(
        self, 
        repo_imagenes: ImagenSiniestroRepositoryPort, 
        repo_siniestros: SiniestroRepositoryPort,
        storage: StoragePort
    ):
        self.repo_imagenes = repo_imagenes
        self.repo_siniestros = repo_siniestros
        self.storage = storage

    def execute(self, siniestro_id: str, file_bytes: bytes, filename: str, content_type: str) -> ImagenSiniestroModel:
        siniestro = self.repo_siniestros.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")

        # 1. Subir imagen a storage
        file_path = f"siniestros/{siniestro_id}/{uuid.uuid4()}_{filename}"
        public_url = self.storage.upload_file(
            bucket_name="imagenes", 
            file_path=file_path, 
            file_bytes=file_bytes, 
            content_type=content_type
        )

        # 2. IA pre-validación de calidad (Para MVP se simula asíncrono o predeterminado a True)
        es_calidad_valida = True
        
        # 3. Guardar registro en base de datos
        imagen = ImagenSiniestroModel(
            id=str(uuid.uuid4()),
            siniestro_id=siniestro_id,
            imagen_url=public_url,
            es_calidad_valida=es_calidad_valida,
            metadatos_json={"original_filename": filename, "content_type": content_type},
            version=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            deleted_at=None
        )
        return self.repo_imagenes.save(imagen)
