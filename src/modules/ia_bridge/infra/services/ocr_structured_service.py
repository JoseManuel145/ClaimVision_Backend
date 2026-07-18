import httpx
import json
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
                error_detail = self._extract_error_detail(e.response)
                raise ThirdPartyServiceError(f"Servicio de IA: {error_detail}")

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
                error_detail = self._extract_error_detail(e.response)
                raise ThirdPartyServiceError(f"Servicio de IA: {error_detail}")

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
                error_detail = self._extract_error_detail(e.response)
                raise ThirdPartyServiceError(f"Servicio de IA: {error_detail}")

    def _extract_error_detail(self, response: httpx.Response) -> str:
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                if "detail" in error_data:
                    detail = error_data["detail"]
                    if isinstance(detail, dict):
                        error_msg = detail.get("error", "")
                        details_list = detail.get("details", [])
                        suggestion = detail.get("suggestion", "")
                        parts = [error_msg]
                        if details_list:
                            parts.extend(details_list)
                        if suggestion:
                            parts.append(f"Sugerencia: {suggestion}")
                        return " | ".join(parts)
                    return str(detail)
                return str(error_data)
            return str(error_data)
        except Exception:
            return f"Error HTTP {response.status_code}"
