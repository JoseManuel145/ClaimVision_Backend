from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class VehiculoResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    aseguradora_id: str
    cliente_id: str
    marca: str
    modelo: str
    anio: int
    placas: str
    vin: Optional[str] = None
    color: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class VehiculoCreateDTO(BaseModel):
    cliente_id: str
    marca: str = Field(..., min_length=1, max_length=100)
    modelo: str = Field(..., min_length=1, max_length=100)
    anio: int = Field(..., ge=1900, le=2030)
    placas: str = Field(..., min_length=5, max_length=10)
    vin: Optional[str] = Field(None, max_length=17)
    color: Optional[str] = Field(None, max_length=50)


class VehiculoUpdateDTO(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    placas: Optional[str] = None
    vin: Optional[str] = None
    color: Optional[str] = None
