import httpx
from typing import Any
from src.core.exceptions import ThirdPartyServiceError


class TranscribirService:
    def __init__(self, ia_url: str):
        self.ia_url = ia_url

    async def transcribe(self, audio_bytes: bytes, filename: str, content_type: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                files = {"file": (filename, audio_bytes, content_type)}
                response = await client.post(
                    f"{self.ia_url}/api/v1/nlp/transcribir",
                    files=files,
                    timeout=120.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")

    async def get_status(self, job_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.ia_url}/api/v1/nlp/transcribir/status/{job_id}",
                    timeout=30.0,
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
                    f"{self.ia_url}/api/v1/nlp/history",
                    params={"page": page, "limit": limit},
                    timeout=30.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")

    async def get_detail(self, job_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.ia_url}/api/v1/nlp/{job_id}",
                    timeout=30.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")
