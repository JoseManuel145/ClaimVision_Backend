import uuid
from supabase import Client
from src.core.config import settings
from src.core.logging import get_logger
from src.modules.taller.domain.ports.pdf_storage_port import PdfStoragePort
from src.core.exceptions import ThirdPartyServiceError

logger = get_logger("storage")


class SupabasePdfStorage(PdfStoragePort):
    def __init__(self, client: Client):
        self.client = client
        self.bucket_name = settings.SUPABASE_BUCKET_PDF

    def upload_pdf(self, file_bytes: bytes, filename: str, content_type: str = "application/pdf") -> str:
        unique_path = f"{uuid.uuid4()}_{filename}"

        try:
            self.client.storage.from_(self.bucket_name).upload(
                file=file_bytes,
                path=unique_path,
                file_options={"content-type": content_type},
            )
        except Exception as e:
            logger.error(f"Error al subir PDF a Supabase Storage (bucket={self.bucket_name}): {e}")
            raise ThirdPartyServiceError(
                detail=f"Error al subir el archivo al almacenamiento: {type(e).__name__}"
            )

        try:
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(unique_path)
        except Exception as e:
            logger.error(f"Error al obtener URL pública del PDF: {e}")
            raise ThirdPartyServiceError(detail="El archivo se subió pero no se pudo obtener la URL pública.")

        return public_url
