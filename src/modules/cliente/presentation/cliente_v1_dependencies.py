from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.imagen_siniestro_repository import ImagenSiniestroRepository
from src.modules.siniestro.infra.adapters.cliente_checker_adapter import ClienteCheckerAdapter
from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository

from src.modules.siniestro.application.siniestros.inicializar_siniestro import InicializarSiniestro
from src.modules.siniestro.application.siniestros.list_siniestros_cliente import ListSiniestrosCliente
from src.modules.siniestro.application.siniestros.get_siniestro_cliente import GetSiniestroCliente
from src.modules.siniestro.application.siniestros.registrar_imagen import RegistrarImagenSiniestro
from src.modules.cliente.application.get_perfil_cliente import GetPerfilCliente
from src.modules.auth.application.confirm_consent import ConfirmConsent
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository


def _cliente_checker(session: Session) -> ClienteCheckerAdapter:
    return ClienteCheckerAdapter(ClienteRepository(session))


def reportar_siniestro_service(session: Session = Depends(get_session)) -> InicializarSiniestro:
    return InicializarSiniestro(SiniestroRepository(session), _cliente_checker(session))


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


def confirm_consent_service(session: Session = Depends(get_session)) -> ConfirmConsent:
    return ConfirmConsent(ClienteRepository(session), AuthRepository(session))
