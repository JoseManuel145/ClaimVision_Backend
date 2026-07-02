from fastapi import APIRouter, Depends, Query, Request, status

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.domain.transitions import construir_timeline
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.siniestro.presentation.siniestros.siniestro_dto import (
    SiniestroInicializarDTO,
    SiniestroResponseDTO,
    ImagenSiniestroResponseDTO,
)
from src.modules.auth.presentation.schemas import ConsentRequestDTO
from src.modules.cliente.presentation.v1.cliente_v1_schemas import (
    RegistrarImagenRequest,
    ConsentimientosRequest,
    PerfilClienteResponse,
    SiniestroDetalleClienteDTO,
)
from src.modules.cliente.presentation.v1.cliente_v1_dependencies import (
    reportar_siniestro_service,
    list_siniestros_cliente_service,
    get_siniestro_cliente_service,
    registrar_imagen_service,
    get_perfil_cliente_service,
    confirm_consent_service,
)

router = APIRouter(prefix="/cliente", tags=["v1 · Cliente"])

get_cliente = require_roles("Cliente")
EVENTO = "cliente.siniestros"


@router.post("/siniestros", response_model=SiniestroResponseDTO, status_code=status.HTTP_201_CREATED)
def reportar_siniestro(
    dto: SiniestroInicializarDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_cliente),
    uc=Depends(reportar_siniestro_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§4 · Reporte preliminar → estatus = Reportado_Preliminar."""
    siniestro = uc.execute(cliente_id=user.usuario_id, aseguradora_id=user.aseguradora_id, dto=dto)
    audit.record(
        evento_modulo=EVENTO, accion="reportar_siniestro", usuario=user,
        request=request, metadata={"siniestro_id": siniestro.id},
    )
    return siniestro


@router.get("/siniestros", response_model=Page[SiniestroResponseDTO])
def listar_mis_siniestros(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    estatus: str | None = Query(None),
    user: AuthenticatedUser = Depends(get_cliente),
    uc=Depends(list_siniestros_cliente_service),
):
    """§4 · Mis siniestros (paginado)."""
    items, total = uc.execute(user.usuario_id, offset_from_page(page, page_size), page_size, estatus)
    data = [SiniestroResponseDTO.model_validate(s) for s in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/siniestros/{id}", response_model=SiniestroDetalleClienteDTO)
def detalle_siniestro(
    id: str,
    user: AuthenticatedUser = Depends(get_cliente),
    uc=Depends(get_siniestro_cliente_service),
):
    """§4 · Seguimiento (detalle + imágenes + timeline de estatus)."""
    siniestro, imagenes = uc.execute(user.usuario_id, id)
    base = SiniestroResponseDTO.model_validate(siniestro)
    return SiniestroDetalleClienteDTO(
        **base.model_dump(),
        imagenes=[ImagenSiniestroResponseDTO.model_validate(i) for i in imagenes],
        timeline=construir_timeline(siniestro.estatus),
    )


@router.post(
    "/siniestros/{id}/imagenes",
    response_model=ImagenSiniestroResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def registrar_imagen(
    id: str,
    dto: RegistrarImagenRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_cliente),
    uc=Depends(registrar_imagen_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§4 · Registra una imagen ya subida (vía URL prefirmada §8)."""
    imagen = uc.execute(user.usuario_id, id, dto.imagen_url, dto.metadatos_json)
    audit.record(
        evento_modulo=EVENTO, accion="registrar_imagen", usuario=user,
        request=request, metadata={"siniestro_id": id, "imagen_id": imagen.id},
    )
    return imagen


@router.get("/perfil", response_model=PerfilClienteResponse)
def get_perfil(
    user: AuthenticatedUser = Depends(get_cliente),
    uc=Depends(get_perfil_cliente_service),
):
    """§4 · Perfil del cliente (numero_poliza, vigencia_poliza, consentimientos)."""
    return uc.execute(user.usuario_id)


@router.patch("/consentimientos", status_code=status.HTTP_200_OK)
def actualizar_consentimientos(
    dto: ConsentimientosRequest,
    request: Request,
    user: AuthenticatedUser = Depends(get_cliente),
    uc=Depends(confirm_consent_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§4 · Registra consentimientos LFPDPPP → setea fecha_consentimiento."""
    uc.execute(
        usuario_id=user.usuario_id,
        data=ConsentRequestDTO(
            aviso_privacidad=dto.consentimiento_aviso_privacidad,
            biometria=dto.consentimiento_biometria,
            transferencia_talleres=dto.autoriza_transferencia_talleres,
        ),
    )
    audit.record(
        evento_modulo="cliente.consentimientos", accion="actualizar_consentimientos",
        usuario=user, request=request,
    )
    return {"message": "Consentimientos registrados exitosamente."}
