import httpx
from typing import Dict, Any
from src.modules.cliente.domain.ports import OcrPort
from src.core.exceptions import ThirdPartyServiceError

class OcrService(OcrPort):
    def __init__(self, ocr_api_url: str):
        self.ocr_api_url = ocr_api_url

    async def extract_data(self, cedula_bytes: bytes, poliza_bytes: bytes) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                files = {
                    "cedula": ("cedula.jpg", cedula_bytes, "image/jpeg"),
                    "poliza": ("poliza.pdf", poliza_bytes, "application/pdf")
                }
                response = await client.post(f"{self.ocr_api_url}/extract", files=files, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicación con el servicio OCR: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio OCR: {e.response.status_code}")
