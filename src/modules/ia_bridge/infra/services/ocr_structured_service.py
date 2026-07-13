import httpx
from typing import Any
from src.core.exceptions import ThirdPartyServiceError


class OcrStructuredService:
    def __init__(self, ia_url: str):
        self.ia_url = ia_url

    async def extract_poliza(self, pdf_bytes: bytes, filename: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                files = {"file": (filename, pdf_bytes, "application/pdf")}
                response = await client.post(
                    f"{self.ia_url}/api/v1/ocr/extract-poliza",
                    files=files,
                    timeout=60.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")

    async def extract_ine(self, file_bytes: bytes, filename: str, content_type: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                files = {"file": (filename, file_bytes, content_type)}
                response = await client.post(
                    f"{self.ia_url}/api/v1/ocr/extract-ine",
                    files=files,
                    timeout=60.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")

    async def extract_and_validate(
        self,
        poliza_bytes: bytes,
        poliza_filename: str,
        ine_bytes: bytes,
        ine_filename: str,
        ine_content_type: str,
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                files = {
                    "poliza": (poliza_filename, poliza_bytes, "application/pdf"),
                    "ine": (ine_filename, ine_bytes, ine_content_type),
                }
                response = await client.post(
                    f"{self.ia_url}/api/v1/ocr/extract-and-validate",
                    files=files,
                    timeout=120.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")
