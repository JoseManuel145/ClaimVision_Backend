from typing import Any
from src.modules.ia_bridge.domain.ports import PredictPort


class PredictAllDamage:
    def __init__(self, predict_port: PredictPort):
        self.predict_port = predict_port

    async def execute(self, files: list[tuple[str, bytes, str]]) -> dict[str, Any]:
        return await self.predict_port.predict_all(files)
