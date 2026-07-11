from typing import Any
from src.modules.ia_bridge.domain.ports import TranscribirPort


class TranscribeAudio:
    def __init__(self, transcribir_port: TranscribirPort):
        self.transcribir_port = transcribir_port

    async def execute(self, audio_bytes: bytes, filename: str, content_type: str) -> dict[str, Any]:
        return await self.transcribir_port.transcribe(audio_bytes, filename, content_type)

    async def get_status(self, job_id: str) -> dict[str, Any]:
        return await self.transcribir_port.get_status(job_id)
