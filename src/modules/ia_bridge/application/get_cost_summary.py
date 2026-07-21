from typing import Any
from src.modules.ia_bridge.domain.ports import PredictPort


class GetCostSummary:
    def __init__(self, predict_port: PredictPort):
        self.predict_port = predict_port

    async def execute(self, danos: list[dict[str, str]]) -> dict[str, Any]:
        return await self.predict_port.get_resumen(danos)
