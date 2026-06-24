from pydantic import BaseModel, ConfigDict


class TallaDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    talla_id: int
    nombre: str


class TallaCreateDTO(BaseModel):
    nombre: str


class TallaUpdateDTO(BaseModel):
    nombre: str | None


class ProductoTallaCreateDTO(BaseModel):
    producto_id: str
    talla_id: int


class ProductoTallaDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    producto_talla_id: int
    producto_id: str
    talla_id: int
