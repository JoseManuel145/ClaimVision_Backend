from typing import Any
from src.modules.ia_bridge.domain.ports import PredictPort


class GetPredictionHistory:
    def __init__(self, predict_port: PredictPort):
        self.predict_port = predict_port

    async def execute(self, page: int, limit: int) -> dict[str, Any]:
        return await self.predict_port.get_history(page, limit)
