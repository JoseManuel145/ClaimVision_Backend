from src.core.config import settings
from src.modules.ia_bridge.infra.services.predict_service import PredictService
from src.modules.ia_bridge.infra.services.ocr_service import IaOcrService
from src.modules.ia_bridge.infra.services.ocr_structured_service import OcrStructuredService
from src.modules.ia_bridge.infra.services.transcribir_service import TranscribirService
from src.modules.ia_bridge.infra.services.analizar_service import AnalizarService
from src.modules.ia_bridge.application.predict_damage import PredictDamage
from src.modules.ia_bridge.application.extract_text import ExtractText
from src.modules.ia_bridge.application.extract_poliza_data import ExtractPolizaData
from src.modules.ia_bridge.application.extract_ine_data import ExtractIneData
from src.modules.ia_bridge.application.extract_and_validate_data import ExtractAndValidateData
from src.modules.ia_bridge.application.transcribe_audio import TranscribeAudio
from src.modules.ia_bridge.application.analyze_text import AnalyzeText


def predict_service():
    port = PredictService(settings.IA_SERVICE_URL)
    return PredictDamage(port)


def ia_ocr_service():
    port = IaOcrService(settings.IA_SERVICE_URL)
    return ExtractText(port)


def ia_ocr_structured_service():
    port = OcrStructuredService(settings.IA_SERVICE_URL)
    return port


def extract_poliza_service():
    port = OcrStructuredService(settings.IA_SERVICE_URL)
    return ExtractPolizaData(port)


def extract_ine_service():
    port = OcrStructuredService(settings.IA_SERVICE_URL)
    return ExtractIneData(port)


def extract_and_validate_service():
    port = OcrStructuredService(settings.IA_SERVICE_URL)
    return ExtractAndValidateData(port)


def transcribir_service():
    port = TranscribirService(settings.IA_SERVICE_URL)
    return TranscribeAudio(port)


def analizar_service():
    port = AnalizarService(settings.IA_SERVICE_URL)
    return AnalyzeText(port)
