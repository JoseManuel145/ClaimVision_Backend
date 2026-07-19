from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.security import require_roles
from src.core.exceptions import NotFoundError
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.siniestro.presentation.peritaje.peritaje_dto import (
    PeritajeUpsertRequestDTO,
    PeritajeResponseDTO,
)
from src.modules.ajustador.presentation.ajustador_schemas import (
    SiniestroDetalleAjustadorDTO,
    EditarPeritajeRequest,
    AjustadorPerfilUpdateRequest,
    DisponibilidadRequest,
    GeolocalizacionRequest,
    AjustadorPerfilResponse,
    DanoRequest,
)
from src.shared.domain.services.encryption_service import encrypt_fields
from src.modules.auth.infra.db.tables.user_table import UserTable
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
from src.modules.ajustador.presentation import ajustador_dependencies as deps
from src.shared.infra.storage.url_resolver import resolve_storage_url
from src.core.supabase import get_supabase_client
from src.shared.domain.models import AccionAudit

router = APIRouter()

get_ajustador = require_roles("Ajustador")
EVENTO = "ajustador"


def _perfil_dto(aj) -> AjustadorPerfilResponse:
    lat, lng = (aj.geolocalizacion_actual or (None, None))
    return AjustadorPerfilResponse(
        id=aj.id, usuario_id=aj.usuario_id, cedula_profesional=aj.cedula_profesional,
        activo_para_servicio=aj.activo_para_servicio,
        nombre=aj.nombre, email=aj.email, telefono=aj.telefono,
        latitud=lat, longitud=lng, version=aj.version,
    )


@router.get("/perfil", response_model=AjustadorPerfilResponse)
def get_perfil(
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: GetPerfilAjustador = Depends(deps.get_perfil_ajustador_service),
):
    """§5 · Perfil del ajustador (datos personales + disponibilidad + ubicación)."""
    aj = uc.execute(user.usuario_id)
    return _perfil_dto(aj)


@router.put("/perfil", response_model=AjustadorPerfilResponse)
def actualizar_perfil(
    dto: AjustadorPerfilUpdateRequest,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: ActualizarPerfilAjustador = Depends(deps.actualizar_perfil_ajustador_service),
):
    """§5 · Actualiza datos personales del ajustador (nombre, email, teléfono)."""
    aj = uc.execute(user.usuario_id, nombre=dto.nombre, email=dto.email, telefono=dto.telefono)
    return _perfil_dto(aj)


@router.get("/asignaciones", response_model=Page[SiniestroResponseDTO])
def listar_asignaciones(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: ListMisAsignaciones = Depends(deps.list_asignaciones_service),
):
    """§5 · Siniestros asignados a mí (paginado)."""
    items, total = uc.execute(user.usuario_id, offset_from_page(page, page_size), page_size, estatus)
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=SiniestroDetalleAjustadorDTO)
def detalle_siniestro(
    id: str,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: GetMiSiniestro = Depends(deps.get_siniestro_service),
    client=Depends(get_supabase_client),
):
    """§5 · Detalle + imágenes + peritaje del ajustador (peritaje_ia lo poblará §7)."""
    siniestro, imagenes, peritaje = uc.execute(user.usuario_id, id)
    base = SiniestroResponseDTO.model_validate(siniestro)
    return SiniestroDetalleAjustadorDTO(
        **base.model_dump(),
        imagenes=[
            ImagenSiniestroResponseDTO.model_validate(i)
            .model_copy(update={"imagen_url": resolve_storage_url(client, i.imagen_url)})
            for i in imagenes
        ],
        peritaje=PeritajeResponseDTO.model_validate(peritaje) if peritaje else None,
        peritaje_ia=None,
    )


@router.post("/siniestros/{id}/peritaje", response_model=PeritajeResponseDTO, status_code=status.HTTP_201_CREATED)
def registrar_peritaje(
    id: str,
    dto: PeritajeUpsertRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: RegistrarPeritaje = Depends(deps.registrar_peritaje_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Crea el peritaje y valida el siniestro → estatus = Peritaje_Validado."""
    peritaje = uc.execute(
        usuario_id=user.usuario_id,
        siniestro_id=id,
        costo_definitivo=dto.costo_definitivo_ajustador,
        firma=dto.firma_digital_ajustador,
        observaciones=dto.observaciones_campo,
        danos_data=[d.model_dump() for d in dto.danos],
    )
    audit.record(
        evento_modulo=EVENTO, accion=AccionAudit.REGISTRAR_PERITAJE, usuario=user, request=request,
        metadata={"siniestro_id": id, "peritaje_id": peritaje.id},
    )
    return peritaje


@router.patch("/peritajes/{id}", response_model=PeritajeResponseDTO)
def editar_peritaje(
    id: str,
    dto: EditarPeritajeRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: EditarPeritaje = Depends(deps.editar_peritaje_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Edita el borrador del peritaje (antes de validar)."""
    peritaje = uc.execute(
        usuario_id=user.usuario_id, peritaje_id=id,
        costo_definitivo=dto.costo_definitivo_ajustador,
        firma=dto.firma_digital_ajustador,
        observaciones=dto.observaciones_campo,
    )
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.EDITAR_PERITAJE, usuario=user, request=request,
                 metadata={"peritaje_id": id})
    return peritaje


@router.post("/peritajes/{id}/danos", response_model=PeritajeResponseDTO, status_code=status.HTTP_201_CREATED)
def agregar_dano(
    id: str,
    dto: DanoRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: AgregarDano = Depends(deps.agregar_dano_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Agrega un daño manual al peritaje."""
    peritaje = uc.execute(user.usuario_id, id, dto.model_dump())
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.AGREGAR_DANO, usuario=user, request=request,
                 metadata={"peritaje_id": id})
    return peritaje


@router.patch("/disponibilidad", response_model=AjustadorPerfilResponse)
def actualizar_disponibilidad(
    dto: DisponibilidadRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: ActualizarDisponibilidad = Depends(deps.disponibilidad_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Activa/desactiva mi disponibilidad para servicio."""
    aj = uc.execute(user.usuario_id, dto.activo_para_servicio)
    audit.record(evento_modulo=EVENTO, accion=AccionAudit.ACTUALIZAR_DISPONIBILIDAD, usuario=user, request=request,
                 metadata={"activo_para_servicio": dto.activo_para_servicio})
    return _perfil_dto(aj)


@router.put("/geolocalizacion", response_model=AjustadorPerfilResponse)
def actualizar_geolocalizacion(
    dto: GeolocalizacionRequest,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: ActualizarGeolocalizacion = Depends(deps.geolocalizacion_service),
):
    """§5 · Actualiza mi geolocalización (geography Point)."""
    aj = uc.execute(user.usuario_id, dto.latitud, dto.longitud)
    return _perfil_dto(aj)
