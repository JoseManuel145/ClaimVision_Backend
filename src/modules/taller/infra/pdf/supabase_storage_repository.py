import uuid
import asyncio
import httpx
from src.core.config import settings
from src.core.logging import get_logger
from src.modules.taller.domain.ports.pdf_storage_port import PdfStoragePort
from src.core.exceptions import ThirdPartyServiceError

logger = get_logger("storage")


class SupabasePdfStorage(PdfStoragePort):
    """
    Sube PDFs a Supabase Storage usando HTTP directo (httpx).
    No depende de storage3 SDK que tiene bugs de serialización.
    """

    def __init__(self):
        self.bucket_name = settings.SUPABASE_BUCKET_PDF
        self.supabase_url = settings.SUPABASE_URL.rstrip("/")
        self.supabase_key = settings.SUPABASE_KEY

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.supabase_key}",
            "apikey": self.supabase_key,
            "Content-Type": "application/pdf",
        }

    def _do_upload(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        unique_path = f"{uuid.uuid4()}_{filename}"
        upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{unique_path}"

        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.put(
                    upload_url,
                    content=file_bytes,
                    headers={
                        "Authorization": f"Bearer {self.supabase_key}",
                        "apikey": self.supabase_key,
                        "Content-Type": content_type,
                    },
                )
                resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(
                "Error al subir PDF a Supabase Storage "
                "(bucket=%s, path=%s, status=%s, body=%s): %s",
                self.bucket_name, unique_path, e.response.status_code,
                e.response.text[:500], e,
            )
            raise ThirdPartyServiceError(
                detail=f"Error al subir el archivo al almacenamiento (HTTP {e.response.status_code})"
            )
        except httpx.RequestError as e:
            logger.error(
                "Error de conexión al subir PDF a Supabase Storage (bucket=%s): %s",
                self.bucket_name, e,
            )
            raise ThirdPartyServiceError(
                detail=f"Error de conexión al subir el archivo: {e.__class__.__name__}"
            )

        public_url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{unique_path}"
        logger.info(
            "PDF subido exitosamente: bucket=%s path=%s url=%s",
            self.bucket_name, unique_path, public_url,
        )
        return public_url

    async def upload_pdf(self, file_bytes: bytes, filename: str, content_type: str = "application/pdf") -> str:
        return await asyncio.to_thread(self._do_upload, file_bytes, filename, content_type)
