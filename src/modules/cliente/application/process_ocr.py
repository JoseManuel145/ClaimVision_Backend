from typing import Dict, Any
from src.modules.cliente.domain.ports import OcrPort

class ProcessOcr:
    def __init__(self, ocr_port: OcrPort):
        self.ocr_port = ocr_port

    async def execute(self, cedula_bytes: bytes, poliza_bytes: bytes) -> Dict[str, Any]:
        """
        Orquesta la llamada al microservicio externo de OCR.
        Retorna los datos extraídos en crudo (ej: {"curp": "...", "numero_poliza": "..."})
        """
        return await self.ocr_port.extract_data(cedula_bytes, poliza_bytes)
