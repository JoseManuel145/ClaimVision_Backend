from dataclasses import dataclass

@dataclass
class CategoriaModel:
    categoria_id: int | None
    nombre: str
    seccion_id: int
    nombre_seccion: str | None = None