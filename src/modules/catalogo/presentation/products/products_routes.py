from fastapi import APIRouter, Depends

from src.modules.catalogo.presentation.products.product_dto import (
    ProductoDTO,
    ProductoCreateDTO,
    ProductoUpdateDTO
)
from src.modules.catalogo.presentation.products.product_dependencies import (
    create_producto_service,
    update_producto_service,
    delete_producto_service,
    get_product_by_id_service,
    get_all_productos_service,
    get_producto_by_categoria_service,
    change_destacado_service,
    change_status_service
)
from src.modules.catalogo.app.products import (
    ListProducts,
    GetProductoById,
    GetProductoByCategoria,
    CreateProducto,
    UpdateProducto,
    DeleteProducto,
    ChangeDestacado,
    ChangeStatus
)

router = APIRouter()

# --- 1. RUTAS DE COLECCIÓN (Raíz) ---
@router.get("", response_model=list[ProductoDTO])
def list_productos(uc: ListProducts = Depends(get_all_productos_service)):
    return uc.execute()

@router.post("", response_model=ProductoDTO)
def create_producto(dto: ProductoCreateDTO, uc: CreateProducto = Depends(create_producto_service)):
    return uc.execute(dto)


# --- 2. FILTROS Y BÚSQUEDAS ESPECÍFICAS ---
@router.get("/by-categoria/{categoria_id}", response_model=list[ProductoDTO])
def get_productos_by_categoria(
    categoria_id: int,
    uc: GetProductoByCategoria = Depends(get_producto_by_categoria_service)
):
    return uc.execute(categoria_id)


# --- 3. ACCIONES SOBRE RECURSOS (Verbos de negocio) ---
@router.put("/{producto_id}/alter-destacado", response_model=ProductoDTO)
def change_destacado(
    producto_id: str,
    destacado: bool,
    uc: ChangeDestacado = Depends(change_destacado_service)
):
    return uc.execute(producto_id, destacado)

@router.put("/{producto_id}/alter-status", response_model=ProductoDTO)
def change_status(
    producto_id: str,
    status: bool,
    uc: ChangeStatus = Depends(change_status_service)
):
    return uc.execute(producto_id, status)


# --- 4. CRUD BÁSICO (Genéricas / Atrapa-todoo) ---
@router.get("/{producto_id}", response_model=ProductoDTO)
def get_producto_by_id(
    producto_id: str,
    uc: GetProductoById = Depends(get_product_by_id_service)
):
    return uc.execute(producto_id)

@router.put("/{producto_id}", response_model=ProductoDTO)
def update_producto(
    producto_id: str,
    dto: ProductoUpdateDTO,
    uc: UpdateProducto = Depends(update_producto_service)
):
    return uc.execute(producto_id, dto)

@router.delete("/{producto_id}", status_code=204)
def delete_producto(
    producto_id: str,
    uc: DeleteProducto = Depends(delete_producto_service)
):
    uc.execute(producto_id)
    return None