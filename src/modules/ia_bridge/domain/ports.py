from typing import Protocol, Any


class PredictPort(Protocol):
    async def predict(self, image_bytes: bytes, filename: str) -> dict[str, Any]: ...


class OcrPort(Protocol):
    async def extract_text(self, pdf_bytes: bytes, filename: str) -> dict[str, Any]: ...


class TranscribirPort(Protocol):
    async def transcribe(self, audio_bytes: bytes, filename: str) -> dict[str, Any]: ...


class AnalizarPort(Protocol):
    async def analyze(self, text: str) -> dict[str, Any]: ...
