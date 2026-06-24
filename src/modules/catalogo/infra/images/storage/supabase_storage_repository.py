from supabase import Client
import mimetypes
from src.core.config import settings
from src.modules.catalogo.domain.ports import ImageStoragePort

class SupabaseStorageRepository(ImageStoragePort):

    def __init__(self, client: Client):
        self.client = client
        self.bucket = settings.SUPABASE_BUCKET

    def upload(self, content: bytes, path: str) -> str:
        content_type, _ = mimetypes.guess_type(path)
        content_type = content_type or "application/octet-stream"

        self.client.storage.from_(self.bucket).upload(
            path,
            content,
            {"content-type": content_type}
        )
        return path

    def delete(self, path: str) -> None:
        self.client.storage.from_(self.bucket).remove([path])
