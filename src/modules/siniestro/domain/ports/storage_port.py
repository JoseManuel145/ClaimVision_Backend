from typing import Protocol

class StoragePort(Protocol):
    def upload_file(self, bucket_name: str, file_path: str, file_bytes: bytes, content_type: str) -> str:
        """Sube un archivo y retorna su URL pública."""
        ...
