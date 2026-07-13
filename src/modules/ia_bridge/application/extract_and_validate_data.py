from typing import Any
from src.modules.ia_bridge.domain.ports import OcrStructuredPort


class ExtractAndValidateData:
    def __init__(self, ocr_port: OcrStructuredPort):
        self.ocr_port = ocr_port

    async def execute(
        self,
        poliza_bytes: bytes,
        poliza_filename: str,
        ine_bytes: bytes,
        ine_filename: str,
        ine_content_type: str,
    ) -> dict[str, Any]:
        return await self.ocr_port.extract_and_validate(
            poliza_bytes, poliza_filename, ine_bytes, ine_filename, ine_content_type
        )
