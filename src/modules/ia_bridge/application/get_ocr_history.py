from typing import Any
from src.modules.ia_bridge.domain.ports import OcrPort


class GetOcrHistory:
    def __init__(self, ocr_port: OcrPort):
        self.ocr_port = ocr_port

    async def execute(self, page: int, limit: int) -> dict[str, Any]:
        return await self.ocr_port.get_history(page, limit)
