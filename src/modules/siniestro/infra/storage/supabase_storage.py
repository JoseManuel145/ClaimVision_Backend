import os
from supabase import create_client, Client
from src.modules.siniestro.domain.ports.storage_port import StoragePort
from src.core.config import settings # Asumiendo que settings tiene SUPABASE_URL y SUPABASE_KEY

class SupabaseStorageAdapter(StoragePort):
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client

    def upload_file(self, bucket_name: str, file_path: str, file_bytes: bytes, content_type: str) -> str:
        res = self.supabase.storage.from_(bucket_name).upload(
            file_path,
            file_bytes,
            file_options={"content-type": content_type}
        )
        
        # Return public URL so url_resolver can resolve it dynamically with a fresh token
        public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{file_path}"
        return public_url
