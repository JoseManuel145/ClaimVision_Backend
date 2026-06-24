from fastapi import APIRouter
from fastapi.params import Depends

from src.modules.catalogo.app.colors import GetAllColors, CreateColor, GetColorById, UpdateColor, DeleteColor, \
    AsociarColor, GetPColorById, GetColoresByProducto, DesasociarColor
from src.modules.catalogo.presentation.colors.color_dependencies import get_all_colors, create_color, get_color_by_id, \
    update_color, delete_color, asociar_color, get_pcolor_by_id, get_colores_by_producto, desasociar_color
from src.modules.catalogo.presentation.colors.color_dto import ColorDTO, ColorCreateDTO, ColorUpdateDTO, \
    ProductoColorDTO, ProductoColorCreateDTO

router = APIRouter()


@router.get("", response_model=list[ColorDTO])
def get_all_colores(
        uc: GetAllColors = Depends(get_all_colors)
):
    return uc.execute()


@router.post("", response_model=ColorDTO)
def create_color(
        dto: ColorCreateDTO,
        uc: CreateColor = Depends(create_color)
):
    return uc.execute(dto)


@router.get("/{color_id}", response_model=ColorDTO)
def get_color_by_id(
        color_id: int,
        uc: GetColorById = Depends(get_color_by_id)
):
    return uc.execute(color_id)


@router.put("/{color_id}", response_model=ColorDTO)
def update_color(
        color_id: int,
        dto: ColorUpdateDTO,
        uc: UpdateColor = Depends(update_color)
):
    return uc.execute(color_id, dto)


@router.delete("/{color_id}", status_code=204)
def delete_color(
        color_id: int,
        uc: DeleteColor = Depends(delete_color)
):
    return uc.execute(color_id)


# RUTAS DE COLORES Y PRODUCTOS
@router.post("/productos", response_model=ProductoColorDTO)
def assign_color_to_producto(
        dto: ProductoColorCreateDTO,
        uc: AsociarColor = Depends(asociar_color),
):
    return uc.execute(dto)


@router.get("/productos/detalles/{p_color_id}", response_model=ProductoColorDTO)
def get_producto_color_by_id(
        p_color_id: int,
        uc: GetPColorById = Depends(get_pcolor_by_id),
):
    return uc.execute(p_color_id)


@router.get("/productos/{producto_id}", response_model=list[ColorDTO])
def get_colores_by_producto(
        producto_id: str,
        uc: GetColoresByProducto = Depends(get_colores_by_producto),
):
    return uc.execute(producto_id)


@router.delete("/productos/{producto_id}/{color_id}", status_code=204)
def remove_color_from_producto(
        producto_id: str,
        color_id: int,
        uc: DesasociarColor = Depends(desasociar_color),
):
    return uc.execute(producto_id, color_id)
