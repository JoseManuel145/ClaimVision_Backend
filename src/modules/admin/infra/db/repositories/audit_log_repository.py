import uuid
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime, timedelta
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AuditLogRepositoryPort
from src.modules.admin.infra.db.tables.audit_log_table import AuditLogTable
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.core.security import decrypt_xsalsa20

def _to_domain(obj: AuditLogTable, user: UserTable = None) -> AuditLog:
    usuario_rol = None
    usuario_nombre = None
    usuario_email = None
    if user:
        usuario_rol = user.rol.value if hasattr(user.rol, 'value') else user.rol
        if user.nombre_completo_cifrado:
            try:
                usuario_nombre = decrypt_xsalsa20(user.nombre_completo_cifrado)
            except Exception:
                usuario_nombre = "Desconocido"
        usuario_email = user.email

    return AuditLog(
        id=str(obj.id),
        usuario_id=str(obj.usuario_id) if obj.usuario_id else None,
        usuario_rol=usuario_rol,
        usuario_nombre=usuario_nombre,
        usuario_email=usuario_email,
        evento_modulo=obj.evento_modulo,
        accion_realizada=obj.accion_realizada,
        direccion_ip=obj.direccion_ip,
        user_agent=obj.user_agent,
        created_at=obj.created_at,
        metadata_context=obj.metadata_context,
        aseguradora_id=str(obj.aseguradora_id) if obj.aseguradora_id else None
    )

class AuditLogRepository(AuditLogRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def append(self, log: AuditLog) -> AuditLog:
        model = AuditLogTable(
            id=log.id or uuid.uuid4(),
            usuario_id=log.usuario_id,
            evento_modulo=log.evento_modulo,
            accion_realizada=log.accion_realizada,
            direccion_ip=log.direccion_ip,
            user_agent=log.user_agent,
            metadata_context=log.metadata_context,
            aseguradora_id=log.aseguradora_id,
            created_at=log.created_at,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def get_by_entity(self, entidad_afectada: str) -> List[AuditLog]:
        stmt = (
            select(AuditLogTable)
            .where(AuditLogTable.evento_modulo == entidad_afectada)
            .order_by(AuditLogTable.created_at.desc())
        )
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results]

    def list_logs(
        self, 
        offset: int = 0, 
        limit: int = 20, 
        aseguradora_id: str | None = None,
        fecha_inicio: datetime | None = None,
        fecha_fin: datetime | None = None,
        accion_realizada: str | None = None,
        evento_modulo: str | None = None,
        usuario_rol: str | None = None
    ) -> Tuple[List[AuditLog], int]:
        import uuid as _uuid

        filtros = []
        if aseguradora_id:
            filtros.append(AuditLogTable.aseguradora_id == _uuid.UUID(aseguradora_id))
        if fecha_inicio:
            filtros.append(AuditLogTable.created_at >= fecha_inicio)
        if fecha_fin:
            filtros.append(AuditLogTable.created_at <= fecha_fin)
        if accion_realizada:
            filtros.append(AuditLogTable.accion_realizada == accion_realizada)
        if evento_modulo:
            filtros.append(AuditLogTable.evento_modulo == evento_modulo)
            
        join_user = False
        if usuario_rol:
            filtros.append(UserTable.rol == usuario_rol)
            join_user = True

        stmt_base = select(AuditLogTable, UserTable).outerjoin(UserTable, AuditLogTable.usuario_id == UserTable.id)
        if filtros:
            stmt_base = stmt_base.where(*filtros)
            
        count_stmt = select(func.count()).select_from(AuditLogTable)
        if join_user:
            count_stmt = count_stmt.join(UserTable, AuditLogTable.usuario_id == UserTable.id)
        if filtros:
            count_stmt = count_stmt.where(*filtros)

        total = self.db.execute(count_stmt).scalar() or 0

        stmt = stmt_base.order_by(AuditLogTable.created_at.desc()).offset(offset).limit(limit)

        results = self.db.execute(stmt).all()
        return [_to_domain(r[0], r[1]) for r in results], total

    def get_detail(self, log_id: str) -> AuditLog | None:
        import uuid as _uuid
        stmt = select(AuditLogTable, UserTable).outerjoin(UserTable, AuditLogTable.usuario_id == UserTable.id).where(AuditLogTable.id == _uuid.UUID(log_id))
        result = self.db.execute(stmt).first()
        if not result:
            return None
        return _to_domain(result[0], result[1])

    def get_resumen(self, dias: int = 30) -> dict:
        fecha_desde = datetime.now() - timedelta(days=dias)
        
        # total eventos
        total_eventos = self.db.execute(
            select(func.count()).select_from(AuditLogTable)
            .where(AuditLogTable.created_at >= fecha_desde)
        ).scalar() or 0
        
        # accesos_login
        accesos_login = self.db.execute(
            select(func.count()).select_from(AuditLogTable)
            .where(AuditLogTable.created_at >= fecha_desde)
            .where(AuditLogTable.accion_realizada == "login")
        ).scalar() or 0
        
        # cambios_CRUD
        crud_stmt = select(func.count()).select_from(AuditLogTable).where(AuditLogTable.created_at >= fecha_desde).where(
            (AuditLogTable.accion_realizada.like("crear_%")) |
            (AuditLogTable.accion_realizada.like("actualizar_%")) |
            (AuditLogTable.accion_realizada.like("eliminar_%"))
        )
        cambios_CRUD = self.db.execute(crud_stmt).scalar() or 0

        # cambios_configuracion
        config_stmt = select(func.count()).select_from(AuditLogTable).where(AuditLogTable.created_at >= fecha_desde).where(
            (AuditLogTable.accion_realizada.like("%aseguradora%")) |
            (AuditLogTable.accion_realizada.like("%arco%")) |
            (AuditLogTable.accion_realizada.like("%suscripcion%"))
        )
        cambios_configuracion = self.db.execute(config_stmt).scalar() or 0

        return {
            "total_eventos": total_eventos,
            "accesos_login": accesos_login,
            "cambios_configuracion": cambios_configuracion,
            "cambios_CRUD": cambios_CRUD,
            "dias": dias,
            "fecha_desde": fecha_desde
        }
