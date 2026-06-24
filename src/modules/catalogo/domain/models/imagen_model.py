from dataclasses import dataclass

@dataclass
class ImagenModel:
    imagen_id: int | None
    path: str
    orden: int

@dataclass
class ProductoImagenModel:
    producto_imagen_id: int | None
    producto_id: str
    imagen_id: int
    es_principal: bool