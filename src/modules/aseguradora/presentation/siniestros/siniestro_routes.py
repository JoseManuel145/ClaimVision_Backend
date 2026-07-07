from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroResponseDTO,
    SiniestroUpdateDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.siniestro.presentation.peritaje.peritaje_dto import PeritajeResponseDTO
from src.modules.taller.presentation.taller_v1_schemas import CotizacionV1DTO
from src.modules.aseguradora.presentation.siniestros.siniestro_dto import (
    AsignarAjustadorDTO,
    EnviarTallerDTO,
    RechazarCotizacionRequest,
    SiniestroDetalleAseguradoraDTO,
)
from src.modules.aseguradora.application.siniestros.list_siniestros_aseguradora import ListSiniestrosAseguradora
from src.modules.aseguradora.application.siniestros.get_siniestro_aseguradora import GetSiniestroAseguradora
from src.modules.aseguradora.application.siniestros.autorizar_entrega_v1 import AutorizarEntregaV1
from src.modules.aseguradora.application.cotizaciones.aprobar_cotizacion import AprobarCotizacion
from src.modules.aseguradora.application.cotizaciones.rechazar_cotizacion import RechazarCotizacion
from src.modules.aseguradora.presentation.siniestros import siniestro_dependencies as deps
from src.modules.siniestro.application.siniestros.asignar_ajustador import AsignarAjustador
from src.modules.siniestro.application.siniestros.editar_siniestro import EditarSiniestro
from src.modules.siniestro.application.siniestros.enviar_taller import EnviarTaller
from src.modules.siniestro.presentation.siniestros.siniestro_dependencies import (
    asignar_ajustador_service,
    editar_siniestro_service,
    enviar_taller_service,
)

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora"


@router.get("/siniestros", response_model=Page[SiniestroResponseDTO])
def listar_siniestros(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    ajustador_id: str | None = Query(None),
    taller_id: str | None = Query(None),
    q: str | None = Query(None, description="Búsqueda por placas/marca/modelo"),
    user: AuthenticatedUser = Depends(get_operador),
    uc: ListSiniestrosAseguradora = Depends(deps.list_siniestros_service),
):
    items, total = uc.execute(
        user.aseguradora_id, offset_from_page(page, page_size), page_size,
        estatus, ajustador_id, taller_id, q,
    )
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=SiniestroDetalleAseguradoraDTO)
def detalle_siniestro(
    id: str,
    user: AuthenticatedUser = Depends(get_operador),
    uc: GetSiniestroAseguradora = Depends(deps.get_siniestro_service),
):
    siniestro, imagenes, peritaje, cotizacion = uc.execute(id, user.aseguradora_id)
    base = SiniestroResponseDTO.model_validate(siniestro)
    return SiniestroDetalleAseguradoraDTO(
        **base.model_dump(),
        imagenes=[ImagenSiniestroResponseDTO.model_validate(i) for i in imagenes],
        peritaje=PeritajeResponseDTO.model_validate(peritaje) if peritaje else None,
        cotizacion=CotizacionV1DTO.model_validate(cotizacion) if cotizacion else None,
        peritaje_ia=None,
    )


@router.put("/siniestros/{id}", response_model=SiniestroResponseDTO)
def editar_siniestro(
    id: str,
    dto: SiniestroUpdateDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: EditarSiniestro = Depends(editar_siniestro_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(siniestro_id=id, usuario_id=user.usuario_id, rol=user.rol, dto=dto)
    audit.record(evento_modulo=EVENTO, accion="editar_siniestro", usuario=user, request=request,
                 metadata={"siniestro_id": id})
    return siniestro


@router.post("/siniestros/{id}/asignar-ajustador", response_model=SiniestroResponseDTO)
def asignar_ajustador(
    id: str,
    dto: AsignarAjustadorDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: AsignarAjustador = Depends(asignar_ajustador_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(id, dto.ajustador_id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="asignar_ajustador", usuario=user, request=request,
                 metadata={"siniestro_id": id, "ajustador_id": dto.ajustador_id})
    return siniestro


@router.post("/siniestros/{id}/enviar-taller", response_model=SiniestroResponseDTO)
def enviar_taller(
    id: str,
    dto: EnviarTallerDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: EnviarTaller = Depends(enviar_taller_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(id, dto.taller_id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="enviar_taller", usuario=user, request=request,
                 metadata={"siniestro_id": id, "taller_id": dto.taller_id})
    return siniestro


@router.post("/siniestros/{id}/autorizar-entrega", response_model=SiniestroResponseDTO)
def autorizar_entrega(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: AutorizarEntregaV1 = Depends(deps.autorizar_entrega_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    siniestro = uc.execute(id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="autorizar_entrega", usuario=user, request=request,
                 metadata={"siniestro_id": id})
    return siniestro


@router.post("/cotizaciones/{id}/aprobar", response_model=CotizacionV1DTO)
def aprobar_cotizacion(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: AprobarCotizacion = Depends(deps.aprobar_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    cot = uc.execute(id, user.aseguradora_id)
    audit.record(evento_modulo=EVENTO, accion="aprobar_cotizacion", usuario=user, request=request,
                 metadata={"cotizacion_id": id})
    return cot


@router.post("/cotizaciones/{id}/rechazar", response_model=CotizacionV1DTO)
def rechazar_cotizacion(
    id: str,
    dto: RechazarCotizacionRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: RechazarCotizacion = Depends(deps.rechazar_cotizacion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    cot = uc.execute(id, user.aseguradora_id, dto.motivo)
    audit.record(evento_modulo=EVENTO, accion="rechazar_cotizacion", usuario=user, request=request,
                 metadata={"cotizacion_id": id, "motivo": dto.motivo})
    return cot
