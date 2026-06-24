from pydantic import BaseModel, ConfigDict

class SeccionDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    seccion_id: int
    nombre: str

class SeccionCreate(BaseModel):
    nombre: str

class SeccionUpdate(BaseModel):
    nombre: str