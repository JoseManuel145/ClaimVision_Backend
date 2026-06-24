from src.modules.catalogo.domain.ports import TallaPort


class DeleteTalla:
    def __init__(self, repo: TallaPort):
        self.repo = repo

    def execute(self, talla_id: int) -> None:
        return self.repo.delete(talla_id)
