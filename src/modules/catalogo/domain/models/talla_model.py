from dataclasses import dataclass

@dataclass
class TallaModel:
    talla_id: int | None
    nombre: str

@dataclass
class ProductoTallaModel:
    producto_talla_id: int | None
    producto_id: str
    talla_id: int