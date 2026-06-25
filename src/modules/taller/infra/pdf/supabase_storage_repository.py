import uuid
from supabase import Client
from src.core.config import settings
from src.modules.taller.domain.ports.pdf_storage_port import PdfStoragePort

class SupabasePdfStorage(PdfStoragePort):
    def __init__(self, client: Client):
        self.client = client
        self.bucket_name = settings.SUPABASE_BUCKET_PDF

    def upload_pdf(self, file_bytes: bytes, filename: str, content_type: str = "application/pdf") -> str:
        # Generate a unique path to prevent overwriting
        unique_path = f"{uuid.uuid4()}_{filename}"
        
        response = self.client.storage.from_(self.bucket_name).upload(
            file=file_bytes,
            path=unique_path,
            file_options={"content-type": content_type}
        )
        
        # Get the public URL
        public_url = self.client.storage.from_(self.bucket_name).get_public_url(unique_path)
        return public_url
