from pydantic import BaseModel
from typing import Any


class PredictResponse(BaseModel):
    id: str
    filename: str
    tipo_dano: str
    severidad: str
    confianza: float
    created_at: str


class OcrResponse(BaseModel):
    id: str
    filename: str
    text: str
    page_count: int
    created_at: str


class TranscribirResponse(BaseModel):
    job_id: str
    status: str
    progress: int


class AnalizarResponse(BaseModel):
    entidades: list[dict[str, Any]]
