from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.imagen_siniestro_repository import ImagenSiniestroRepository
from src.modules.siniestro.infra.db.repositories.peritaje_repository import PeritajeAjustadorRepository
from src.modules.taller.infra.db.repositories.cotizacion_repository import CotizacionRepository

from src.modules.aseguradora.application.siniestros.list_siniestros_aseguradora import ListSiniestrosAseguradora
from src.modules.aseguradora.application.siniestros.get_siniestro_aseguradora import GetSiniestroAseguradora
from src.modules.aseguradora.application.cotizaciones.aprobar_cotizacion import AprobarCotizacion
from src.modules.aseguradora.application.cotizaciones.rechazar_cotizacion import RechazarCotizacion
from src.modules.aseguradora.application.siniestros.autorizar_entrega_v1 import AutorizarEntregaV1


def list_siniestros_service(session: Session = Depends(get_session)) -> ListSiniestrosAseguradora:
    return ListSiniestrosAseguradora(SiniestroRepository(session))


def get_siniestro_service(session: Session = Depends(get_session)) -> GetSiniestroAseguradora:
    return GetSiniestroAseguradora(
        SiniestroRepository(session),
        ImagenSiniestroRepository(session),
        PeritajeAjustadorRepository(session),
        CotizacionRepository(session),
    )


def aprobar_cotizacion_service(session: Session = Depends(get_session)) -> AprobarCotizacion:
    return AprobarCotizacion(CotizacionRepository(session), SiniestroRepository(session))


def rechazar_cotizacion_service(session: Session = Depends(get_session)) -> RechazarCotizacion:
    return RechazarCotizacion(CotizacionRepository(session), SiniestroRepository(session))


def autorizar_entrega_service(session: Session = Depends(get_session)) -> AutorizarEntregaV1:
    return AutorizarEntregaV1(SiniestroRepository(session))
