from pydantic import BaseModel, field_validator
from fastapi import Form
from src.core.config import settings


class ProductoImagenCreateDTO(BaseModel):
    producto_id: str
    imagen_id: int
    es_principal: bool | None = False


class ImagenCreateDTO(BaseModel):
    orden: int

    @classmethod
    def as_form(cls, orden: int = Form(...)):
        return cls(orden=orden)

class ImagenDTO(BaseModel):
    imagen_id: int
    path: str
    orden: int

    @field_validator("path")
    @classmethod
    def build_url(cls, v: str) -> str:
        return (
            f"{settings.SUPABASE_URL}"
            f"/storage/v1/object/public/"
            f"{settings.SUPABASE_BUCKET}/{v}"
        )

    class Config:
        from_attributes = True


class ProductoImagenDTO(BaseModel):
    producto_imagen_id: int
    producto_id: str
    imagen_id: int
    es_principal: bool

    class Config:
        from_attributes = True
