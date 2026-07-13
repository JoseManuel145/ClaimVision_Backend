from typing import Protocol
from src.modules.cliente.domain.models import ClienteProfile

class ClienteRepositoryPort(Protocol):
    def get_by_usuario_id(self, usuario_id: str) -> ClienteProfile | None: ...
    def save(self, profile: ClienteProfile) -> ClienteProfile: ...
    def update(self, profile: ClienteProfile) -> ClienteProfile: ...

class OcrStructuredPort(Protocol):
    async def extract_and_validate(
        self,
        poliza_bytes: bytes,
        poliza_filename: str,
        ine_bytes: bytes,
        ine_filename: str,
        ine_content_type: str,
    ) -> dict: ...
