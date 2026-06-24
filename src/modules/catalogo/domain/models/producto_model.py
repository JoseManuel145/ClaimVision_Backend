from datetime import datetime
from dataclasses import dataclass, field

from .talla_model import TallaModel
from .imagen_model import ImagenModel
from .color_model import ColorModel

@dataclass
class ProductoModel:
    producto_id: str
    nombre: str
    precio: int
    esta_activo: bool
    esta_destacado: bool
    fecha_creacion: datetime
    stock: int = 0

    imagenes: list[ImagenModel] = field(default_factory=list)
    tallas: list[TallaModel] = field(default_factory=list)
    colores: list[ColorModel] = field(default_factory=list)

    descripcion: str | None = None
    categoria_id: int | None = None