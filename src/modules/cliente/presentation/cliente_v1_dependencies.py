from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.config import settings
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.imagen_siniestro_repository import ImagenSiniestroRepository
from src.modules.siniestro.infra.adapters.cliente_checker_adapter import ClienteCheckerAdapter
from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository
from src.modules.aseguradora.infra.db.repositories.vehiculo_repository import VehiculoRepository
from src.modules.aseguradora.infra.adapters.vehiculo_adapter import VehiculoAdapter
from src.modules.aseguradora.application.vehiculos.list_vehiculos_cliente import ListVehiculosCliente
from src.modules.ia_bridge.infra.services.ocr_structured_service import OcrStructuredService

from src.modules.siniestro.application.siniestros.inicializar_siniestro import InicializarSiniestro
from src.modules.siniestro.application.siniestros.list_siniestros_cliente import ListSiniestrosCliente
from src.modules.siniestro.application.siniestros.get_siniestro_cliente import GetSiniestroCliente
from src.modules.siniestro.application.siniestros.registrar_imagen import RegistrarImagenSiniestro
from src.modules.siniestro.application.siniestros.subir_imagen_siniestro import SubirImagenSiniestro
from src.modules.siniestro.infra.storage.supabase_storage import SupabaseStorageAdapter
from src.core.supabase import get_supabase_client
from src.modules.cliente.application.get_perfil_cliente import GetPerfilCliente
from src.modules.cliente.application.actualizar_perfil_cliente import ActualizarPerfilCliente
from src.modules.cliente.application.create_vehicle_from_poliza import CreateVehicleFromPoliza
from src.modules.auth.application.confirm_consent import ConfirmConsent
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository


def _cliente_checker(session: Session) -> ClienteCheckerAdapter:
    return ClienteCheckerAdapter(ClienteRepository(session))


def cliente_checker_service(session: Session = Depends(get_session)) -> ClienteCheckerAdapter:
    return _cliente_checker(session)


def reportar_siniestro_service(session: Session = Depends(get_session)) -> InicializarSiniestro:
    return InicializarSiniestro(
        SiniestroRepository(session),
        _cliente_checker(session),
        VehiculoRepository(session),
    )


def list_siniestros_cliente_service(session: Session = Depends(get_session)) -> ListSiniestrosCliente:
    return ListSiniestrosCliente(SiniestroRepository(session), _cliente_checker(session))


def get_siniestro_cliente_service(session: Session = Depends(get_session)) -> GetSiniestroCliente:
    return GetSiniestroCliente(
        SiniestroRepository(session),
        ImagenSiniestroRepository(session),
        _cliente_checker(session),
    )


def registrar_imagen_service(session: Session = Depends(get_session)) -> RegistrarImagenSiniestro:
    return RegistrarImagenSiniestro(
        ImagenSiniestroRepository(session),
        SiniestroRepository(session),
        _cliente_checker(session),
    )


def get_perfil_cliente_service(session: Session = Depends(get_session)) -> GetPerfilCliente:
    return GetPerfilCliente(ClienteRepository(session))


def get_auth_repo_for_enrichment(session: Session = Depends(get_session)):
    from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
    return AuthRepository(session)


def actualizar_perfil_cliente_service(session: Session = Depends(get_session)) -> ActualizarPerfilCliente:
    return ActualizarPerfilCliente(ClienteRepository(session), AuthRepository(session))


def confirm_consent_service(session: Session = Depends(get_session)) -> ConfirmConsent:
    return ConfirmConsent(ClienteRepository(session), AuthRepository(session))


def list_vehiculos_cliente_service(session: Session = Depends(get_session)) -> ListVehiculosCliente:
    return ListVehiculosCliente(
        VehiculoAdapter(VehiculoRepository(session)),
        _cliente_checker(session),
    )


def subir_imagen_siniestro_service(
    session: Session = Depends(get_session),
    client=Depends(get_supabase_client),
) -> SubirImagenSiniestro:
    return SubirImagenSiniestro(
        ImagenSiniestroRepository(session),
        SiniestroRepository(session),
        SupabaseStorageAdapter(client),
    )


def create_vehicle_from_poliza_service(
    session: Session = Depends(get_session),
) -> CreateVehicleFromPoliza:
    ocr_port = OcrStructuredService(settings.IA_SERVICE_URL)
    vehiculo_adapter = VehiculoAdapter(VehiculoRepository(session))
    cliente_repo = ClienteRepository(session)
    return CreateVehicleFromPoliza(ocr_port, vehiculo_adapter, cliente_repo)
