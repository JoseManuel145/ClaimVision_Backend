import os
from supabase import create_client, Client
from src.modules.siniestro.domain.ports.storage_port import StoragePort
from src.core.config import settings
from src.shared.infra.storage.url_resolver import resolve_bucket


class SupabaseStorageAdapter(StoragePort):
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    def upload_file(self, bucket_name: str | None, file_path: str, file_bytes: bytes, content_type: str) -> str:
        if not bucket_name:
            bucket_name = resolve_bucket(file_path)

        res = self.supabase.storage.from_(bucket_name).upload(
            file_path,
            file_bytes,
            file_options={"content-type": content_type}
        )

        public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{file_path}"
        return public_url
