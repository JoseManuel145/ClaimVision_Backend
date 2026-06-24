import uuid
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AuditLogRepositoryPort
from src.modules.admin.infra.db.tables.audit_log_table import AuditLogTable

def _to_domain(obj: AuditLogTable) -> AuditLog:
    return AuditLog(
        id=str(obj.id),
        usuario_id=str(obj.usuario_id) if obj.usuario_id else None,
        evento_modulo=obj.evento_modulo,
        accion_realizada=obj.accion_realizada,
        direccion_ip=obj.direccion_ip,
        user_agent=obj.user_agent,
        created_at=obj.created_at,
        metadata_context=obj.metadata_context,
        aseguradora_id=str(obj.aseguradora_id)
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

    def list_logs(self, offset: int = 0, limit: int = 20) -> Tuple[List[AuditLog], int]:
        count_stmt = select(func.count()).select_from(AuditLogTable)
        total = self.db.execute(count_stmt).scalar() or 0

        stmt = (
            select(AuditLogTable)
            .order_by(AuditLogTable.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        results = self.db.execute(stmt).scalars().all()
        return [_to_domain(r) for r in results], total
