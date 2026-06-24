from src.modules.catalogo.domain.ports.categoria_port import CategoriaPort


class DeleteCategory:
    def __init__(self, repo: CategoriaPort):
        self.repo = repo

    def execute(self, categoria_id: int) -> None:
        return self.repo.delete(categoria_id)
