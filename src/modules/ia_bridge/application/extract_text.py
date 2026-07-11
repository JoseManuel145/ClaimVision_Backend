from typing import Any
from src.modules.ia_bridge.domain.ports import OcrPort


class ExtractText:
    def __init__(self, ocr_port: OcrPort):
        self.ocr_port = ocr_port

    async def execute(self, pdf_bytes: bytes, filename: str) -> dict[str, Any]:
        return await self.ocr_port.extract_text(pdf_bytes, filename)
