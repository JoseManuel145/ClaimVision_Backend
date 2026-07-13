from typing import Any
from src.modules.ia_bridge.domain.ports import OcrStructuredPort


class ExtractPolizaData:
    def __init__(self, ocr_port: OcrStructuredPort):
        self.ocr_port = ocr_port

    async def execute(self, pdf_bytes: bytes, filename: str) -> dict[str, Any]:
        return await self.ocr_port.extract_poliza(pdf_bytes, filename)
