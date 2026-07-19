from typing import List, Tuple
from datetime import datetime
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AuditLogRepositoryPort

class ConsultarAuditoriaUseCase:
    def __init__(self, audit_repo: AuditLogRepositoryPort):
        self.audit_repo = audit_repo

    def execute(
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
        return self.audit_repo.list_logs(
            offset=offset, 
            limit=limit, 
            aseguradora_id=aseguradora_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            accion_realizada=accion_realizada,
            evento_modulo=evento_modulo,
            usuario_rol=usuario_rol
        )
        
    def get_detail(self, log_id: str) -> AuditLog | None:
        return self.audit_repo.get_detail(log_id)
        
    def get_resumen(self, dias: int = 30) -> dict:
        return self.audit_repo.get_resumen(dias=dias)


