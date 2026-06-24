from src.modules.catalogo.domain.models import ColorModel
from src.modules.catalogo.domain.ports import ColorPort


class GetAllColors:
    def __init__(self, repo: ColorPort):
        self.repo = repo

    def execute(self) -> list[ColorModel]:
        return self.repo.get_all()