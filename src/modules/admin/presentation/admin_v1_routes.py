from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.core.database import get_session
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.admin.presentation.schemas import (
    AseguradoraRequestDTO,
    AseguradoraResponseDTO,
    UpdateSuscripcionDTO,
    UpdateAseguradoraDTO,
    AuditResponse,
    OperadorAseguradoraRequestDTO,
    CreateUsuarioRequestDTO,
    UpdateUsuarioRequestDTO,
    UsuarioResponseDTO,
    TallerAdminResponseDTO,
    DashboardResumenDTO,
    EstatusCountDTO,
    SiniestrosPorMesDTO,
)
from src.modules.admin.application.registrar_aseguradora import RegistrarAseguradoraUseCase
from src.modules.admin.application.crear_operador_aseguradora import CrearOperadorAseguradoraUseCase
from src.modules.admin.application.list_aseguradoras import ListAseguradoras
from src.modules.admin.application.get_aseguradora_by_id import GetAseguradoraById
from src.modules.admin.application.actualizar_aseguradora import ActualizarAseguradoraUseCase
from src.modules.admin.application.verificar_aseguradora import VerificarAseguradoraUseCase
from src.modules.admin.application.actualizar_suscripcion import ActualizarSuscripcionUseCase
from src.modules.admin.application.desincorporar_aseguradora import DesincorporarAseguradoraUseCase
from src.modules.admin.application.aplicar_bloqueo_arco import AplicarBloqueoArcoUseCase
from src.modules.admin.application.consultar_auditoria import ConsultarAuditoriaUseCase
from src.modules.admin.application.list_usuarios import ListUsuarios
from src.modules.admin.application.get_usuario import GetUsuario
from src.modules.admin.application.create_usuario import CreateUsuario
from src.modules.admin.application.update_usuario import UpdateUsuario
from src.modules.admin.application.delete_usuario import DeleteUsuario
from src.modules.admin.application.list_talleres_admin import ListTalleresAdmin
from src.modules.admin.application.get_taller_admin import GetTallerAdmin
from src.modules.admin.application.get_dashboard_resumen import GetDashboardResumen
from src.modules.admin.presentation import dependencies as deps

from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository
from src.modules.aseguradora.infra.db.tables.convenio_table import ConvenioAseguradoraTallerTable
from src.modules.admin.infra.db.tables.aseguradora_table import AseguradoraTable

router = APIRouter()

get_admin = require_roles("Administrador_Global")

EVENTO = "admin"


# ── Aseguradoras CRUD ──────────────────────────────────────────────────

@router.post("/aseguradoras", response_model=AseguradoraResponseDTO, status_code=status.HTTP_201_CREATED)
def registrar_aseguradora(
    data: AseguradoraRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: RegistrarAseguradoraUseCase = Depends(deps.registrar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Registrar una nueva aseguradora en la plataforma."""
    resultado = uc.execute(user.usuario_id, data)
    audit.record(
        evento_modulo=EVENTO, accion="registrar_aseguradora",
        usuario=user, request=request,
        metadata={"aseguradora_id": resultado.id},
    )
    return resultado


@router.post("/aseguradoras/{aseguradora_id}/operadores", status_code=status.HTTP_201_CREATED)
def crear_operador_aseguradora(
    aseguradora_id: str,
    data: OperadorAseguradoraRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: CrearOperadorAseguradoraUseCase = Depends(deps.crear_operador_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Crear un operador para una aseguradora específica."""
    resultado = uc.execute(user.usuario_id, aseguradora_id, data)
    audit.record(
        evento_modulo=EVENTO, accion="crear_operador",
        usuario=user, request=request,
        metadata={"aseguradora_id": aseguradora_id},
    )
    return resultado


@router.get("/aseguradoras", response_model=Page[AseguradoraResponseDTO])
def listar_aseguradoras(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    include_deleted: bool = Query(False, description="Incluir aseguradoras desincorporadas"),
    user: AuthenticatedUser = Depends(get_admin),
    uc: ListAseguradoras = Depends(deps.list_aseguradoras_service),
):
    """§5 · Listar aseguradoras registradas (paginado, con filtro de baja)."""
    offset = offset_from_page(page, page_size)
    items, total = uc.execute(offset=offset, limit=page_size, include_deleted=include_deleted)
    data = [AseguradoraResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/aseguradoras/desincorporadas", response_model=Page[AseguradoraResponseDTO])
def listar_aseguradoras_desincorporadas(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_admin),
    uc: ListAseguradoras = Depends(deps.list_aseguradoras_service),
):
    """§5 · Listar únicamente aseguradoras desincorporadas (baja lógica)."""
    offset = offset_from_page(page, page_size)
    items, total = uc.execute(offset=offset, limit=page_size, include_deleted=True)
    deleted = [i for i in items if i.deleted_at is not None or i.estatus_comercial == "Cancelado"]
    data = [AseguradoraResponseDTO.model_validate(i) for i in deleted]
    return Page.build(data=data, total=len(deleted), page=page, page_size=page_size)


@router.get("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO)
def obtener_aseguradora(
    aseguradora_id: str,
    user: AuthenticatedUser = Depends(get_admin),
    uc: GetAseguradoraById = Depends(deps.get_aseguradora_by_id_service),
):
    """§5 · Obtener detalle de una aseguradora por ID."""
    try:
        return uc.execute(user.usuario_id, aseguradora_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO)
def actualizar_aseguradora(
    aseguradora_id: str,
    data: UpdateAseguradoraDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: ActualizarAseguradoraUseCase = Depends(deps.actualizar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Actualizar datos de una aseguradora existente."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id, data)
        audit.record(
            evento_modulo=EVENTO, accion="actualizar_aseguradora",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/aseguradoras/{aseguradora_id}/verificar", response_model=AseguradoraResponseDTO)
def verificar_aseguradora(
    aseguradora_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: VerificarAseguradoraUseCase = Depends(deps.verificar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Marcar aseguradora como verificada."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id)
        audit.record(
            evento_modulo=EVENTO, accion="verificar_aseguradora",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/aseguradoras/{aseguradora_id}/suscripcion", response_model=AseguradoraResponseDTO)
def actualizar_suscripcion(
    aseguradora_id: str,
    data: UpdateSuscripcionDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: ActualizarSuscripcionUseCase = Depends(deps.actualizar_suscripcion_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Actualizar plan de suscripción de una aseguradora."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id, data)
        audit.record(
            evento_modulo=EVENTO, accion="actualizar_suscripcion",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id, "nuevo_plan": data.nuevo_plan},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/aseguradoras/{aseguradora_id}", response_model=AseguradoraResponseDTO)
def desincorporar_aseguradora(
    aseguradora_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: DesincorporarAseguradoraUseCase = Depends(deps.desincorporar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Desincorporar (baja lógica) una aseguradora de la plataforma."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id)
        audit.record(
            evento_modulo=EVENTO, accion="desincorporar_aseguradora",
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── Usuarios (ARCO) ──────────────────────────────────────────────────

@router.post("/usuarios/{usuario_id}/bloqueo-arco")
def aplicar_bloqueo_arco(
    usuario_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: AplicarBloqueoArcoUseCase = Depends(deps.aplicar_bloqueo_arco_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§6 · Aplicar bloqueo ARCO a un usuario (cifra sus datos personales)."""
    try:
        uc.execute(user.usuario_id, usuario_id)
        audit.record(
            evento_modulo=EVENTO, accion="bloqueo_arco",
            usuario=user, request=request,
            metadata={"usuario_id": usuario_id},
        )
        return {"message": "Usuario bloqueado y datos cifrados exitosamente por derechos ARCO."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── Auditoría ─────────────────────────────────────────────────────────

@router.get("/auditoria/logs", response_model=Page[AuditResponse])
def consultar_auditoria(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_admin),
    uc: ConsultarAuditoriaUseCase = Depends(deps.consultar_auditoria_service),
):
    """§6 · Consultar logs de auditoría (paginado)."""
    try:
        offset = offset_from_page(page, page_size)
        items, total = uc.execute(offset=offset, limit=page_size)
        data = [AuditResponse.model_validate(i) for i in items]
        return Page.build(data=data, total=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ── Usuarios CRUD ─────────────────────────────────────────────────────

@router.get("/usuarios", response_model=Page[UsuarioResponseDTO])
def listar_usuarios(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    rol: Optional[str] = Query(None, description="Filtrar por rol"),
    estatus: Optional[str] = Query(None, description="Filtrar por estatus_arco"),
    search: Optional[str] = Query(None, description="Buscar por email o nombre"),
    user: AuthenticatedUser = Depends(get_admin),
    uc: ListUsuarios = Depends(deps.list_usuarios_service),
):
    """Listar usuarios con paginación y filtros."""
    offset = offset_from_page(page, page_size)
    items, total = uc.execute(offset=offset, limit=page_size, rol=rol, estatus=estatus, search=search)
    data = [UsuarioResponseDTO.model_validate(i) for i in items]
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponseDTO)
def obtener_usuario(
    usuario_id: str,
    user: AuthenticatedUser = Depends(get_admin),
    uc: GetUsuario = Depends(deps.get_usuario_service),
):
    """Obtener detalle de un usuario por ID."""
    try:
        return UsuarioResponseDTO.model_validate(uc.execute(usuario_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/usuarios", response_model=UsuarioResponseDTO, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    data: CreateUsuarioRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: CreateUsuario = Depends(deps.create_usuario_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """Crear un nuevo usuario con cualquier rol."""
    try:
        resultado = uc.execute(user.usuario_id, data)
        audit.record(
            evento_modulo=EVENTO, accion="crear_usuario",
            usuario=user, request=request,
            metadata={"usuario_id": resultado["id"]},
        )
        return UsuarioResponseDTO.model_validate(resultado)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponseDTO)
def actualizar_usuario(
    usuario_id: str,
    data: UpdateUsuarioRequestDTO,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: UpdateUsuario = Depends(deps.update_usuario_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """Actualizar datos de un usuario existente."""
    try:
        resultado = uc.execute(user.usuario_id, usuario_id, data)
        audit.record(
            evento_modulo=EVENTO, accion="actualizar_usuario",
            usuario=user, request=request,
            metadata={"usuario_id": usuario_id},
        )
        return UsuarioResponseDTO.model_validate(resultado)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/usuarios/{usuario_id}", response_model=UsuarioResponseDTO)
def eliminar_usuario(
    usuario_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: DeleteUsuario = Depends(deps.delete_usuario_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """Baja lógica de un usuario (valida que no tenga siniestros activos)."""
    try:
        resultado = uc.execute(user.usuario_id, usuario_id)
        audit.record(
            evento_modulo=EVENTO, accion="eliminar_usuario",
            usuario=user, request=request,
            metadata={"usuario_id": usuario_id, "soft_delete": True},
        )
        return UsuarioResponseDTO.model_validate(resultado)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


# ── Talleres (admin global) ──────────────────────────────────────────

@router.get("/talleres", response_model=Page[TallerAdminResponseDTO])
def listar_talleres_admin(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_admin),
    uc: ListTalleresAdmin = Depends(deps.list_talleres_admin_service),
    db_session=Depends(get_session),
):
    """Listar todos los talleres del sistema (sin filtro por aseguradora)."""
    offset = offset_from_page(page, page_size)
    items, total = uc.execute(offset=offset, limit=page_size)

    taller_ids = [t.id for t in items]
    convenios_map = {}
    if taller_ids:
        from sqlalchemy import select as sa_select
        rows = db_session.execute(
            sa_select(ConvenioAseguradoraTallerTable.aseguradora_id, ConvenioAseguradoraTallerTable.taller_id)
            .where(ConvenioAseguradoraTallerTable.taller_id.in_(taller_ids))
            .where(ConvenioAseguradoraTallerTable.deleted_at.is_(None))
        ).all()
        for row in rows:
            tid = str(row.taller_id)
            if tid not in convenios_map:
                convenios_map[tid] = []
            convenios_map[tid].append(str(row.aseguradora_id))

    data = []
    for t in items:
        data.append(TallerAdminResponseDTO(
            id=t.id,
            nombre_comercial=t.nombre_comercial,
            rfc=t.rfc,
            direccion_tecnica=t.direccion_tecnica,
            telefono_contacto=t.telefono_contacto,
            aseguradoras_vinculadas=convenios_map.get(t.id, []),
            created_at=t.created_at,
            updated_at=t.updated_at,
            deleted_at=t.deleted_at,
        ))
    return Page.build(data=data, total=total, page=page, page_size=page_size)


@router.get("/talleres/{taller_id}", response_model=TallerAdminResponseDTO)
def obtener_taller_admin(
    taller_id: str,
    user: AuthenticatedUser = Depends(get_admin),
    uc: GetTallerAdmin = Depends(deps.get_taller_admin_service),
    db_session=Depends(get_session),
):
    """Obtener detalle de un taller con aseguradoras vinculadas."""
    try:
        taller = uc.execute(taller_id)
        from sqlalchemy import select as sa_select
        rows = db_session.execute(
            sa_select(ConvenioAseguradoraTallerTable.aseguradora_id)
            .where(ConvenioAseguradoraTallerTable.taller_id == taller_id)
            .where(ConvenioAseguradoraTallerTable.deleted_at.is_(None))
        ).all()
        aseguradoras = [str(r.aseguradora_id) for r in rows]
        return TallerAdminResponseDTO(
            id=taller.id,
            nombre_comercial=taller.nombre_comercial,
            rfc=taller.rfc,
            direccion_tecnica=taller.direccion_tecnica,
            telefono_contacto=taller.telefono_contacto,
            aseguradoras_vinculadas=aseguradoras,
            created_at=taller.created_at,
            updated_at=taller.updated_at,
            deleted_at=taller.deleted_at,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ── Dashboard ─────────────────────────────────────────────────────────

@router.get("/dashboard/resumen", response_model=DashboardResumenDTO)
def obtener_dashboard_resumen(
    user: AuthenticatedUser = Depends(get_admin),
    uc: GetDashboardResumen = Depends(deps.get_dashboard_resumen_service),
):
    """KPIs globales del sistema."""
    try:
        resultado = uc.execute()
        return DashboardResumenDTO(**resultado)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
