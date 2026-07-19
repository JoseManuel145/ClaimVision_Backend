from typing import Any
from src.modules.ia_bridge.domain.ports import PredictPort, UnsupervisedPort


class GetSupervisedHealth:
    def __init__(self, predict_port: PredictPort):
        self.predict_port = predict_port

    async def execute(self) -> dict[str, Any]:
        return await self.predict_port.get_health()


class GetUnsupervisedHealth:
    def __init__(self, unsupervised_port: UnsupervisedPort):
        self.unsupervised_port = unsupervised_port

    async def execute(self) -> dict[str, Any]:
        return await self.unsupervised_port.get_health()
