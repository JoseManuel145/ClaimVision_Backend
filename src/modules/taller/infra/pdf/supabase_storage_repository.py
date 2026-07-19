import uuid
import asyncio
from supabase import Client
from src.core.config import settings
from src.core.logging import get_logger
from src.modules.taller.domain.ports.pdf_storage_port import PdfStoragePort
from src.core.exceptions import ThirdPartyServiceError

logger = get_logger("storage")

SIGNED_URL_TTL = 3600  # 1 hora


class SupabasePdfStorage(PdfStoragePort):
    """
    Sube PDFs a Supabase Storage via el SDK oficial.
    Genera URLs firmadas con expiracion de 1 hora.
    """

    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.bucket_name = settings.SUPABASE_BUCKET_PDF

    def _do_upload(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        unique_path = f"{uuid.uuid4()}_{filename}"

        try:
            self.supabase.storage.from_(self.bucket_name).upload(
                unique_path,
                file_bytes,
                file_options={"content-type": content_type, "upsert": "false"},
            )
        except Exception as e:
            logger.error(
                "Error al subir PDF a Supabase Storage "
                "(bucket=%s, path=%s): %s",
                self.bucket_name, unique_path, e,
            )
            raise ThirdPartyServiceError(
                detail=f"Error al subir el archivo al almacenamiento: {e}"
            )

        signed_res = self.supabase.storage.from_(self.bucket_name).create_signed_url(
            unique_path, SIGNED_URL_TTL
        )
        signed_url = signed_res['signedURL']

        logger.info(
            "PDF subido exitosamente: bucket=%s path=%s url=%s",
            self.bucket_name, unique_path, signed_url,
        )
        return signed_url

    async def upload_pdf(self, file_bytes: bytes, filename: str, content_type: str = "application/pdf") -> str:
        return await asyncio.to_thread(self._do_upload, file_bytes, filename, content_type)
