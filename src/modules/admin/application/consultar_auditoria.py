from typing import List
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.domain.ports import AuditLogRepositoryPort

class ConsultarAuditoriaUseCase:
    def __init__(self, audit_repo: AuditLogRepositoryPort):
        self.audit_repo = audit_repo

    def execute(self) -> List[AuditLog]:
        return self.audit_repo.list_logs()
