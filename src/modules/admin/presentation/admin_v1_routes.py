from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from src.core.database import get_session
from src.core.security import require_roles
from src.core.exceptions import NotFoundError
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.presentation.pagination import Page, offset_from_page
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.admin.presentation.schemas import (
    AseguradoraRequestDTO,
    AseguradoraResponseDTO,
    UpdateSuscripcionDTO,
    UpdateAseguradoraDTO,
    AuditResponse,
    AuditDetailResponse,
    OperadorAseguradoraRequestDTO,
    CreateUsuarioRequestDTO,
    UpdateUsuarioRequestDTO,
    UsuarioResponseDTO,
    TallerAdminResponseDTO,
    DashboardResumenDTO,
    EstatusCountDTO,
    SiniestrosPorMesDTO,
    PurgeAseguradoraResponse,
)
from src.modules.admin.application.registrar_aseguradora import RegistrarAseguradoraUseCase
from src.modules.admin.application.crear_operador_aseguradora import CrearOperadorAseguradoraUseCase
from src.modules.admin.application.list_aseguradoras import ListAseguradoras
from src.modules.admin.application.get_aseguradora_by_id import GetAseguradoraById
from src.modules.admin.application.actualizar_aseguradora import ActualizarAseguradoraUseCase
from src.modules.admin.application.verificar_aseguradora import VerificarAseguradoraUseCase
from src.modules.admin.application.actualizar_suscripcion import ActualizarSuscripcionUseCase
from src.modules.admin.application.desincorporar_aseguradora import DesincorporarAseguradoraUseCase
from src.modules.admin.application.reactivar_aseguradora import ReactivarAseguradoraUseCase
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
from src.modules.admin.application.purge_aseguradora import PurgeAseguradoraUseCase
from src.modules.admin.presentation import dependencies as deps

from src.modules.aseguradora.infra.db.repositories.taller_repository import TallerRepository
from src.modules.aseguradora.infra.db.tables.convenio_table import ConvenioAseguradoraTallerTable
from src.modules.admin.infra.db.tables.aseguradora_table import AseguradoraTable

router = APIRouter()

get_admin = require_roles("Administrador_Global")
get_admin_or_operador = require_roles("Administrador_Global", "Operador_Aseguradora")

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
        evento_modulo=EVENTO, accion=AccionAudit.REGISTRAR_ASEGURADORA,
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
        evento_modulo=EVENTO, accion=AccionAudit.CREAR_OPERADOR,
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
            evento_modulo=EVENTO, accion=AccionAudit.ACTUALIZAR_ASEGURADORA,
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
            evento_modulo=EVENTO, accion=AccionAudit.VERIFICAR_ASEGURADORA,
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
            evento_modulo=EVENTO, accion=AccionAudit.ACTUALIZAR_SUSCRIPCION,
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
            evento_modulo=EVENTO, accion=AccionAudit.DESINCORPORAR_ASEGURADORA,
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id},
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/aseguradoras/{aseguradora_id}/reactivar", response_model=AseguradoraResponseDTO)
def reactivar_aseguradora(
    aseguradora_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: ReactivarAseguradoraUseCase = Depends(deps.reactivar_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """§5 · Reactivar una aseguradora desincorporada (baja lógica)."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id)
        audit.record(
            evento_modulo=EVENTO, accion=AccionAudit.REACTIVAR_ASEGURADORA,
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
            evento_modulo=EVENTO, accion=AccionAudit.BLOQUEO_ARCO,
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
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None),
    accion_realizada: Optional[str] = Query(None),
    evento_modulo: Optional[str] = Query(None),
    usuario_rol: Optional[str] = Query(None),
    user: AuthenticatedUser = Depends(get_admin_or_operador),
    uc: ConsultarAuditoriaUseCase = Depends(deps.consultar_auditoria_service),
):
    """§6 · Consultar logs de auditoría (paginado)."""
    try:
        from datetime import datetime
        
        fi = datetime.fromisoformat(fecha_inicio.replace("Z", "+00:00")) if fecha_inicio else None
        ff = datetime.fromisoformat(fecha_fin.replace("Z", "+00:00")) if fecha_fin else None
        
        offset = offset_from_page(page, page_size)
        if user.rol == "Operador_Aseguradora":
            filtro_aseg = user.aseguradora_id
        else:
            filtro_aseg = None
            
        items, total = uc.execute(
            offset=offset, limit=page_size, aseguradora_id=filtro_aseg,
            fecha_inicio=fi, fecha_fin=ff, accion_realizada=accion_realizada,
            evento_modulo=evento_modulo, usuario_rol=usuario_rol
        )
        data = [AuditResponse.model_validate(i) for i in items]
        return Page.build(data=data, total=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/auditoria/logs/export")
def exportar_auditoria_csv(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None),
    accion_realizada: Optional[str] = Query(None),
    evento_modulo: Optional[str] = Query(None),
    usuario_rol: Optional[str] = Query(None),
    user: AuthenticatedUser = Depends(get_admin_or_operador),
    uc: ConsultarAuditoriaUseCase = Depends(deps.consultar_auditoria_service),
):
    """§6 · Exportar logs de auditoría en formato CSV."""
    from fastapi.responses import StreamingResponse
    import csv
    import io
    from datetime import datetime

    try:
        fi = datetime.fromisoformat(fecha_inicio.replace("Z", "+00:00")) if fecha_inicio else None
        ff = datetime.fromisoformat(fecha_fin.replace("Z", "+00:00")) if fecha_fin else None
        
        if user.rol == "Operador_Aseguradora":
            filtro_aseg = user.aseguradora_id
        else:
            filtro_aseg = None
            
        # Export limit up to 10000 records
        items, _ = uc.execute(
            offset=0, limit=10000, aseguradora_id=filtro_aseg,
            fecha_inicio=fi, fecha_fin=ff, accion_realizada=accion_realizada,
            evento_modulo=evento_modulo, usuario_rol=usuario_rol
        )
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Usuario_ID", "Rol", "Nombre", "Email", "Aseguradora_ID", "Modulo", "Accion", "IP", "User_Agent", "Fecha"])
        for item in items:
            writer.writerow([
                item.id, item.usuario_id, item.usuario_rol, item.usuario_nombre, item.usuario_email,
                item.aseguradora_id, item.evento_modulo, item.accion_realizada, item.direccion_ip,
                item.user_agent, item.created_at.isoformat()
            ])
            
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=auditoria.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/auditoria/logs/{log_id}", response_model=AuditDetailResponse)
def consultar_auditoria_detalle(
    log_id: str,
    user: AuthenticatedUser = Depends(get_admin_or_operador),
    uc: ConsultarAuditoriaUseCase = Depends(deps.consultar_auditoria_service),
):
    """§6 · Obtener el detalle de un log de auditoría."""
    item = uc.get_detail(log_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Log not found")
    if user.rol == "Operador_Aseguradora" and item.aseguradora_id != user.aseguradora_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access to this log")
    return AuditDetailResponse.model_validate(item)

from src.modules.admin.presentation.schemas import AuditoriaResumenResponse
from src.shared.domain.models import AccionAudit

@router.get("/auditoria/resumen", response_model=AuditoriaResumenResponse)
def consultar_auditoria_resumen(
    dias: int = Query(30, ge=1, le=365),
    user: AuthenticatedUser = Depends(get_admin),
    uc: ConsultarAuditoriaUseCase = Depends(deps.consultar_auditoria_service),
):
    """§6 · Obtener un resumen/KPIs de la auditoría."""
    try:
        resultado = uc.get_resumen(dias=dias)
        return AuditoriaResumenResponse(**resultado)
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
            evento_modulo=EVENTO, accion=AccionAudit.CREAR_USUARIO,
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
            evento_modulo=EVENTO, accion=AccionAudit.ACTUALIZAR_USUARIO,
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
            evento_modulo=EVENTO, accion=AccionAudit.ELIMINAR_USUARIO,
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


# ── Purge ──────────────────────────────────────────────────────────────

@router.post("/aseguradoras/{aseguradora_id}/purge", response_model=PurgeAseguradoraResponse)
def purgar_aseguradora(
    aseguradora_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_admin),
    uc: PurgeAseguradoraUseCase = Depends(deps.purge_aseguradora_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    """Eliminar todos los datos asociados a una aseguradora (baja total)."""
    try:
        resultado = uc.execute(user.usuario_id, aseguradora_id)
        audit.record(
            evento_modulo=EVENTO, accion=AccionAudit.PURGA_ASEGURADORA,
            usuario=user, request=request,
            metadata={"aseguradora_id": aseguradora_id, "deleted": resultado["deleted"]},
        )
        return PurgeAseguradoraResponse(**resultado)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error interno durante la purga. Revise los logs.")


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
