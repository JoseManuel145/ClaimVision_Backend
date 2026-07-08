from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.imagen_siniestro_repository import ImagenSiniestroRepository
from src.modules.siniestro.infra.db.repositories.peritaje_repository import PeritajeAjustadorRepository
from src.modules.aseguradora.infra.db.repositories.ajustador_repository import AjustadorRepository

from src.modules.ajustador.application.list_mis_asignaciones import ListMisAsignaciones
from src.modules.ajustador.application.get_mi_siniestro import GetMiSiniestro
from src.modules.ajustador.application.registrar_peritaje import RegistrarPeritaje
from src.modules.ajustador.application.editar_peritaje import EditarPeritaje
from src.modules.ajustador.application.agregar_dano import AgregarDano
from src.modules.ajustador.application.actualizar_disponibilidad import ActualizarDisponibilidad
from src.modules.ajustador.application.actualizar_geolocalizacion import ActualizarGeolocalizacion
from src.modules.ajustador.application.get_perfil_ajustador import GetPerfilAjustador
from src.modules.ajustador.application.actualizar_perfil_ajustador import ActualizarPerfilAjustador
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository


def get_perfil_ajustador_service(session: Session = Depends(get_session)) -> GetPerfilAjustador:
    return GetPerfilAjustador(AjustadorRepository(session))


def actualizar_perfil_ajustador_service(session: Session = Depends(get_session)) -> ActualizarPerfilAjustador:
    return ActualizarPerfilAjustador(AjustadorRepository(session), AuthRepository(session))


def list_asignaciones_service(session: Session = Depends(get_session)) -> ListMisAsignaciones:
    return ListMisAsignaciones(AjustadorRepository(session), SiniestroRepository(session))


def get_siniestro_service(session: Session = Depends(get_session)) -> GetMiSiniestro:
    return GetMiSiniestro(
        AjustadorRepository(session),
        SiniestroRepository(session),
        ImagenSiniestroRepository(session),
        PeritajeAjustadorRepository(session),
    )


def registrar_peritaje_service(session: Session = Depends(get_session)) -> RegistrarPeritaje:
    return RegistrarPeritaje(
        AjustadorRepository(session),
        SiniestroRepository(session),
        PeritajeAjustadorRepository(session),
    )


def editar_peritaje_service(session: Session = Depends(get_session)) -> EditarPeritaje:
    return EditarPeritaje(
        AjustadorRepository(session),
        SiniestroRepository(session),
        PeritajeAjustadorRepository(session),
    )


def agregar_dano_service(session: Session = Depends(get_session)) -> AgregarDano:
    return AgregarDano(
        AjustadorRepository(session),
        SiniestroRepository(session),
        PeritajeAjustadorRepository(session),
    )


def disponibilidad_service(session: Session = Depends(get_session)) -> ActualizarDisponibilidad:
    return ActualizarDisponibilidad(AjustadorRepository(session))


def geolocalizacion_service(session: Session = Depends(get_session)) -> ActualizarGeolocalizacion:
    return ActualizarGeolocalizacion(AjustadorRepository(session))
