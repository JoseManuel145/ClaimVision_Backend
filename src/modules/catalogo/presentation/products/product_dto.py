from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.modules.catalogo.presentation.images.images_dto import ImagenDTO
from src.modules.catalogo.presentation.sizes.talla_dto import TallaDTO
from src.modules.catalogo.presentation.colors.color_dto import ColorDTO


class ProductoDTO(BaseModel):
    # Usamos ConfigDict para Pydantic V2 (es lo más moderno)
    model_config = ConfigDict(from_attributes=True)

    producto_id: str | None = None
    nombre: str
    precio: int
    descripcion: str | None = None
    esta_activo: bool
    esta_destacado: bool
    stock: int = 0
    categoria_id: int | None = None
    fecha_creacion: datetime
    imagenes: list[ImagenDTO] = []
    tallas: list[TallaDTO] =  []
    colores: list[ColorDTO] = []

class ProductoCreateDTO(BaseModel):
    nombre: str
    precio: int
    descripcion: str | None = None
    esta_activo: bool
    esta_destacado: bool
    stock: int = 0
    categoria_id: int

class ProductoUpdateDTO(BaseModel):
    # En un Update, all suele ser opcional porque puedes actualizar solo un campo
    nombre: str | None = None
    precio: int | None = None
    descripcion: str | None = None
    esta_activo: bool | None = None
    esta_destacado: bool | None = None
    stock: int | None = None
    categoria_id: int | None = None