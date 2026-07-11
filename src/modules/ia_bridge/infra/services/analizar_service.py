import httpx
from typing import Any
from src.core.exceptions import ThirdPartyServiceError


class AnalizarService:
    def __init__(self, ia_url: str):
        self.ia_url = ia_url

    async def analyze(self, text: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.ia_url}/api/v1/nlp/analizar",
                    json={"texto": text},
                    timeout=60.0,
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise ThirdPartyServiceError(f"Error de comunicacion con el servicio de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise ThirdPartyServiceError(f"Error en la respuesta del servicio de IA: {e.response.status_code}")
