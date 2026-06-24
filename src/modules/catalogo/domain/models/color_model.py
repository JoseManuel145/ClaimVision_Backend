from dataclasses import dataclass

@dataclass
class ColorModel:
    color_id: int | None
    nombre: str

@dataclass
class ProductoColorModel:
    producto_color_id: int | None
    producto_id: str
    color_id: int
