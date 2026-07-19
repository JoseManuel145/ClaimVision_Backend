import httpx
from typing import Any
from src.core.exceptions import ThirdPartyServiceError


class IaOcrService:
    def __init__(self, ia_url: str):
        self.ia_url = ia_url

    async def extract_text(self, pdf_bytes: bytes, filename: str, content_type: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                files = {"file": (filename, pdf_bytes, content_type)}
                response = await client.post(
                    f"{self.ia_url}/api/v1/ocr",
                    files=files,
                    timeout=60.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")

    async def get_history(self, page: int, limit: int) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.ia_url}/api/v1/ocr/history",
                    params={"page": page, "limit": limit},
                    timeout=30.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")
