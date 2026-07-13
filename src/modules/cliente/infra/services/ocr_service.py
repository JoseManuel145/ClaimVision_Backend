from src.modules.ia_bridge.infra.services.ocr_structured_service import OcrStructuredService


class ClienteOcrStructuredService:
    def __init__(self, ia_service_url: str):
        self._delegate = OcrStructuredService(ia_service_url)

    async def extract_and_validate(
        self,
        poliza_bytes: bytes,
        poliza_filename: str,
        ine_bytes: bytes,
        ine_filename: str,
        ine_content_type: str,
    ) -> dict:
        return await self._delegate.extract_and_validate(
            poliza_bytes,
            poliza_filename,
            ine_bytes,
            ine_filename,
            ine_content_type,
        )
