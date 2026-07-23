from typing import Protocol

class StoragePort(Protocol):
    def upload_file(self, bucket_name: str | None, file_path: str, file_bytes: bytes, content_type: str) -> str:
        """Sube un archivo y retorna su URL pública. Si bucket_name es None, se resuelve automáticamente por el path."""
        ...
