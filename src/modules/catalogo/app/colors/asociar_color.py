from src.modules.catalogo.domain.models import ProductoColorModel
from src.modules.catalogo.domain.ports import ProductoColorPort
from src.modules.catalogo.presentation.colors.color_dto import ProductoColorCreateDTO


class AsociarColor:
    def __init__(self, repo: ProductoColorPort):
        self.repo = repo

    def execute(self, dto: ProductoColorCreateDTO) -> ProductoColorModel:
        model = ProductoColorModel(
            producto_color_id=None,
            producto_id=dto.producto_id,
            color_id=dto.color_id
        )
        return self.repo.assign_to_producto(model)