from src.modules.admin.domain.models import AseguradoraTenant
from src.modules.admin.domain.ports import AseguradoraRepositoryPort
from src.core.exceptions import NotFoundError

class GetAseguradoraById:
    def __init__(self, repo: AseguradoraRepositoryPort):
        self.repo = repo

    def execute(self, admin_id: str, aseguradora_id: str) -> AseguradoraTenant:
        tenant = self.repo.get_by_id(aseguradora_id)
        if not tenant:
            raise NotFoundError("Aseguradora no encontrada.")
        return tenant
