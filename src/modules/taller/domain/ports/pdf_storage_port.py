from typing import Protocol

class PdfStoragePort(Protocol):
    def upload_pdf(self, file_bytes: bytes, filename: str, content_type: str = "application/pdf") -> str: ...
