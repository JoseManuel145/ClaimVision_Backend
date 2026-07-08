from typing import List, Tuple, Optional
from src.modules.admin.domain.ports import AdminUserRepositoryPort

class ListUsuarios:
    def __init__(self, user_repo: AdminUserRepositoryPort):
        self.user_repo = user_repo

    def execute(
        self,
        offset: int = 0,
        limit: int = 20,
        rol: Optional[str] = None,
        estatus: Optional[str] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[dict], int]:
        return self.user_repo.list_all(offset=offset, limit=limit, rol=rol, estatus=estatus, search=search)
