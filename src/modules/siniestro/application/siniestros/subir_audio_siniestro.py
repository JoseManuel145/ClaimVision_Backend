import uuid
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.storage_port import StoragePort
from src.core.exceptions import NotFoundError

class SubirAudioSiniestro:
    def __init__(
        self,
        repo_siniestros: SiniestroRepositoryPort,
        storage: StoragePort,
    ):
        self.repo_siniestros = repo_siniestros
        self.storage = storage

    def execute(self, siniestro_id: str, audio_bytes: bytes, filename: str, content_type: str) -> str:
        siniestro = self.repo_siniestros.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")

        file_path = f"siniestros/{siniestro_id}/audio_{uuid.uuid4()}_{filename}"
        public_url = self.storage.upload_file(
            bucket_name="imagenes",
            file_path=file_path,
            file_bytes=audio_bytes,
            content_type=content_type or "audio/wav",
        )

        siniestro.narracion_audio_url = public_url
        self.repo_siniestros.update(siniestro)
        return public_url
