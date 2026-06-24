from fastapi import Depends
from src.core.database import get_session
from src.core.config import settings
from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository
from src.modules.cliente.infra.services.ocr_service import OcrService
from src.modules.cliente.application.process_ocr import ProcessOcr
from src.modules.cliente.application.confirm_data import ConfirmData

def process_ocr_service():
    ocr_port = OcrService(settings.OCR_API_URL)
    return ProcessOcr(ocr_port)

def confirm_data_service(session=Depends(get_session)):
    repo = ClienteRepository(session)
    return ConfirmData(repo)
