from src.core.exceptions import NotFoundError


class GetPerfilAseguradora:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, aseguradora_id: str):
        aseg = self.repo.get_by_id(aseguradora_id)
        if not aseg:
            raise NotFoundError("Aseguradora no encontrada.")
        return aseg
