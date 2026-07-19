from typing import Any
from src.modules.ia_bridge.domain.ports import TranscribirPort


class GetNlpHistory:
    def __init__(self, transcribir_port: TranscribirPort):
        self.transcribir_port = transcribir_port

    async def execute(self, page: int, limit: int) -> dict[str, Any]:
        return await self.transcribir_port.get_history(page, limit)
