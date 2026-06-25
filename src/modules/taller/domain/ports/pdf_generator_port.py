from typing import Protocol, Any, Dict

class PdfGeneratorPort(Protocol):
    def generate_pdf(self, context: Dict[str, Any]) -> bytes: ...
