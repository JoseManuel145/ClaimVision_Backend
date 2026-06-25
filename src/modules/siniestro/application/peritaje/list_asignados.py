from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort

class ListSiniestrosAsignados:
    def __init__(self, siniestro_repo: SiniestroRepositoryPort):
        self.siniestro_repo = siniestro_repo

    async def execute(self, ajustador_id: str, offset: int = 0, limit: int = 20, estatus: str | None = None):
        return self.siniestro_repo.list_by_ajustador(ajustador_id, offset, limit, estatus)
