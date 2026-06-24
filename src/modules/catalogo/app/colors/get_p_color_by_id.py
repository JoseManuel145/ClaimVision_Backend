from src.modules.catalogo.domain.models import ProductoColorModel
from src.modules.catalogo.domain.ports import ProductoColorPort


class GetPColorById:
    def __init__(self, repo: ProductoColorPort):
        self.repo = repo

    def execute(self, p_color_id: int) -> ProductoColorModel | None:
        p_color = self.repo.get_by_id(p_color_id)
        if not p_color:
            raise ValueError(f"No existe {p_color_id}")
        return p_color
