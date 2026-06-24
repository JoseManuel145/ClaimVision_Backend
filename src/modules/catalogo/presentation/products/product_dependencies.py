from fastapi import Depends

from src.core.database import get_session
from src.modules.catalogo.app.images.get_images import GetImages
from src.modules.catalogo.app.products import (
    ListProducts,
    GetProductoById,
    GetProductoByCategoria,
    CreateProducto,
    DeleteProducto,
    UpdateProducto,
    ChangeStatus,
    ChangeDestacado,
)
from src.modules.catalogo.infra.images.db.image_repository import ImageRepository
from src.modules.catalogo.infra.images.db.product_image_repository import ProductImageRepository
from src.modules.catalogo.infra.products.product_repository import ProductoRepository


def get_all_productos_service(session=Depends(get_session)):
    producto_repo = ProductoRepository(session)
    return ListProducts(producto_repo)


def get_product_by_id_service(session=Depends(get_session)):
    producto_repo = ProductoRepository(session)
    return GetProductoById(producto_repo)


def get_producto_by_categoria_service(session=Depends(get_session)):
    imagen_repo = ImageRepository(session)
    product_image_repo = ProductImageRepository(session)
    get_images_uc = GetImages(imagen_repo, product_image_repo)
    producto_repo = ProductoRepository(session)
    return GetProductoByCategoria(producto_repo, get_images_uc)


def create_producto_service(session=Depends(get_session)):
    repo = ProductoRepository(session)
    return CreateProducto(repo)


def delete_producto_service(session=Depends(get_session)):
    repo = ProductoRepository(session)
    return DeleteProducto(repo)


def update_producto_service(session=Depends(get_session)):
    repo = ProductoRepository(session)
    return UpdateProducto(repo)


def change_status_service(session=Depends(get_session)):
    repo = ProductoRepository(session)
    return ChangeStatus(repo)


def change_destacado_service(session=Depends(get_session)):
    repo = ProductoRepository(session)
    return ChangeDestacado(repo)
