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
        
        # Generar la URL pública
        url_res = self.supabase.storage.from_(bucket_name).get_public_url(file_path)
        return url_res
