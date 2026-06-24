from src.modules.catalogo.domain.models import ProductoModel
from src.modules.catalogo.domain.ports import ProductoPort
from src.modules.catalogo.presentation.products.product_dto import ProductoUpdateDTO


class UpdateProducto:
    def __init__(self, repo: ProductoPort):
        self.repo = repo

    def execute(self, producto_id: str, dto: ProductoUpdateDTO) -> ProductoModel:
        producto = self.repo.get_by_id(producto_id)
        if not producto:
            raise ValueError(f'Producto {producto_id} no existe')
        producto.nombre = dto.nombre
        producto.precio = dto.precio
        producto.descripcion = dto.descripcion
        producto.esta_activo = dto.esta_activo
        producto.esta_destacado = dto.esta_destacado
        producto.categoria_id = dto.categoria_id
        return self.repo.update_producto(producto_id, producto)