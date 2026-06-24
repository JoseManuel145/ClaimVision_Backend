from uuid import uuid4
from datetime import datetime
from src.modules.catalogo.domain.ports import ProductoPort
from src.modules.catalogo.domain.models import ProductoModel
from src.modules.catalogo.presentation.products.product_dto import ProductoCreateDTO

class CreateProducto:
    def __init__(self, repo: ProductoPort):
        self.repo = repo
        
    def execute(self, dto: ProductoCreateDTO) -> ProductoModel:
        producto = ProductoModel(
            producto_id=str(uuid4()),
            nombre=dto.nombre,
            precio=dto.precio,
            descripcion=dto.descripcion,
            esta_activo=dto.esta_activo,
            esta_destacado=dto.esta_destacado,
            categoria_id=dto.categoria_id,
            fecha_creacion=datetime.now()
        )
        return self.repo.create_producto(producto)