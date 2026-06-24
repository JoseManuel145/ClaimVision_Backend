from src.modules.catalogo.domain.ports import ColorPort


class DeleteColor:
    def __init__(self, repo: ColorPort):
        self.repo = repo

    def execute(self, color_id: int) -> None:
        return self.repo.delete(color_id)
