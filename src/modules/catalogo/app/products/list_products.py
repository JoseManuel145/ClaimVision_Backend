from src.modules.catalogo.domain.models import ProductoModel
from src.modules.catalogo.domain.ports import ProductoPort


class ListProducts:
    def __init__(self, repo: ProductoPort):
        self.repo = repo

    def execute(self) -> list[ProductoModel]:
        productos = self.repo.get_all()
        return productos
