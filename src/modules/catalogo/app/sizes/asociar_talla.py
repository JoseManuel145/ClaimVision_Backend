from src.modules.catalogo.domain.models import ProductoTallaModel
from src.modules.catalogo.domain.ports.talla_port import ProductoTallaPort
from src.modules.catalogo.presentation.sizes.talla_dto import ProductoTallaCreateDTO


class AsociarTalla:
    def __init__(self, repo: ProductoTallaPort):
        self.repo = repo

    def execute(self, dto: ProductoTallaCreateDTO) -> ProductoTallaModel:
        model = ProductoTallaModel(
            producto_talla_id=None,
            producto_id=dto.producto_id,
            talla_id=dto.talla_id
        )
        return self.repo.assign_to_producto(model)