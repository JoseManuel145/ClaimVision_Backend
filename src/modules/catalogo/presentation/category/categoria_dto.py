from pydantic import BaseModel, ConfigDict


class CategoriaDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    categoria_id: int
    nombre: str
    seccion_id: int
    nombre_seccion: str | None = None


class CategoriaCreate(BaseModel):
    nombre: str
    seccion_id: int


class CategoriaUpdate(BaseModel):
    nombre: str
    seccion_id: int
