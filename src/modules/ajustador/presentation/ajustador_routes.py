from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
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
    DisponibilidadRequest,
    GeolocalizacionRequest,
    AjustadorPerfilResponse,
    DanoRequest,
)
from src.modules.ajustador.presentation import ajustador_dependencies as deps

router = APIRouter(prefix="/ajustador", tags=["v1 · Ajustador"])

get_ajustador = require_roles("Ajustador")
EVENTO = "ajustador"


def _perfil_dto(aj) -> AjustadorPerfilResponse:
    lat, lng = (aj.geolocalizacion_actual or (None, None))
    return AjustadorPerfilResponse(
        id=aj.id, usuario_id=aj.usuario_id, cedula_profesional=aj.cedula_profesional,
        activo_para_servicio=aj.activo_para_servicio, latitud=lat, longitud=lng, version=aj.version,
    )


@router.get("/asignaciones", response_model=Page[SiniestroResponseDTO])
def listar_asignaciones(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_ajustador),
    uc=Depends(deps.list_asignaciones_service),
):
    """§5 · Siniestros asignados a mí (paginado)."""
    items, total = uc.execute(user.usuario_id, offset_from_page(page, page_size), page_size, estatus)
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=SiniestroDetalleAjustadorDTO)
def detalle_siniestro(
    id: str,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc=Depends(deps.get_siniestro_service),
):
    """§5 · Detalle + imágenes + peritaje del ajustador (peritaje_ia lo poblará §7)."""
    siniestro, imagenes, peritaje = uc.execute(user.usuario_id, id)
    base = SiniestroResponseDTO.model_validate(siniestro)
    return SiniestroDetalleAjustadorDTO(
        **base.model_dump(),
        imagenes=[ImagenSiniestroResponseDTO.model_validate(i) for i in imagenes],
        peritaje=PeritajeResponseDTO.model_validate(peritaje) if peritaje else None,
        peritaje_ia=None,
    )


@router.post("/siniestros/{id}/peritaje", response_model=PeritajeResponseDTO, status_code=status.HTTP_201_CREATED)
def registrar_peritaje(
    id: str,
    dto: PeritajeUpsertRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc=Depends(deps.registrar_peritaje_service),
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
        evento_modulo=EVENTO, accion="registrar_peritaje", usuario=user, request=request,
        metadata={"siniestro_id": id, "peritaje_id": peritaje.id},
    )
    return peritaje


@router.patch("/peritajes/{id}", response_model=PeritajeResponseDTO)
def editar_peritaje(
    id: str,
    dto: EditarPeritajeRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc=Depends(deps.editar_peritaje_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Edita el borrador del peritaje (antes de validar)."""
    peritaje = uc.execute(
        usuario_id=user.usuario_id, peritaje_id=id,
        costo_definitivo=dto.costo_definitivo_ajustador,
        firma=dto.firma_digital_ajustador,
        observaciones=dto.observaciones_campo,
    )
    audit.record(evento_modulo=EVENTO, accion="editar_peritaje", usuario=user, request=request,
                 metadata={"peritaje_id": id})
    return peritaje


@router.post("/peritajes/{id}/danos", response_model=PeritajeResponseDTO, status_code=status.HTTP_201_CREATED)
def agregar_dano(
    id: str,
    dto: DanoRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc=Depends(deps.agregar_dano_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Agrega un daño manual al peritaje."""
    peritaje = uc.execute(user.usuario_id, id, dto.model_dump())
    audit.record(evento_modulo=EVENTO, accion="agregar_dano", usuario=user, request=request,
                 metadata={"peritaje_id": id})
    return peritaje


@router.patch("/disponibilidad", response_model=AjustadorPerfilResponse)
def actualizar_disponibilidad(
    dto: DisponibilidadRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc=Depends(deps.disponibilidad_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Activa/desactiva mi disponibilidad para servicio."""
    aj = uc.execute(user.usuario_id, dto.activo_para_servicio)
    audit.record(evento_modulo=EVENTO, accion="actualizar_disponibilidad", usuario=user, request=request,
                 metadata={"activo_para_servicio": dto.activo_para_servicio})
    return _perfil_dto(aj)


@router.put("/geolocalizacion", response_model=AjustadorPerfilResponse)
def actualizar_geolocalizacion(
    dto: GeolocalizacionRequest,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc=Depends(deps.geolocalizacion_service),
):
    """§5 · Actualiza mi geolocalización (geography Point)."""
    aj = uc.execute(user.usuario_id, dto.latitud, dto.longitud)
    return _perfil_dto(aj)
