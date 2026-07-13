from fastapi import Depends
from src.core.database import get_session
from src.core.config import settings
from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository
from src.modules.cliente.infra.services.ocr_service import ClienteOcrStructuredService
from src.modules.cliente.application.process_ocr import ProcessOcr
from src.modules.cliente.application.confirm_data import ConfirmData
from src.modules.aseguradora.infra.db.repositories.vehiculo_repository import VehiculoRepository
from src.modules.aseguradora.infra.adapters.vehiculo_adapter import VehiculoAdapter


def process_ocr_service():
    ocr_port = ClienteOcrStructuredService(settings.IA_SERVICE_URL)
    return ProcessOcr(ocr_port)


def confirm_data_service(session=Depends(get_session)):
    repo = ClienteRepository(session)
    vehiculo_adapter = VehiculoAdapter(VehiculoRepository(session))
    return ConfirmData(repo, vehiculo_adapter)
