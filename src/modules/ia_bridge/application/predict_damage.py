from typing import Any
from src.modules.ia_bridge.domain.ports import PredictPort


class PredictDamage:
    def __init__(self, predict_port: PredictPort):
        self.predict_port = predict_port

    async def execute(self, image_bytes: bytes, filename: str) -> dict[str, Any]:
        return await self.predict_port.predict(image_bytes, filename)
