from typing import List, Tuple
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AuditLogRepositoryPort

class ConsultarAuditoriaUseCase:
    def __init__(self, audit_repo: AuditLogRepositoryPort):
        self.audit_repo = audit_repo

    def execute(self, offset: int = 0, limit: int = 20, aseguradora_id: str | None = None) -> Tuple[List[AuditLog], int]:
        return self.audit_repo.list_logs(offset=offset, limit=limit, aseguradora_id=aseguradora_id)

