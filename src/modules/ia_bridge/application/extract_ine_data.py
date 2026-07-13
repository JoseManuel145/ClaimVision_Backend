from typing import Any
from src.modules.ia_bridge.domain.ports import OcrStructuredPort


class ExtractIneData:
    def __init__(self, ocr_port: OcrStructuredPort):
        self.ocr_port = ocr_port

    async def execute(self, file_bytes: bytes, filename: str, content_type: str) -> dict[str, Any]:
        return await self.ocr_port.extract_ine(file_bytes, filename, content_type)
