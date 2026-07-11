from typing import Any
from src.modules.ia_bridge.domain.ports import AnalizarPort


class AnalyzeText:
    def __init__(self, analizar_port: AnalizarPort):
        self.analizar_port = analizar_port

    async def execute(self, text: str) -> dict[str, Any]:
        return await self.analizar_port.analyze(text)
