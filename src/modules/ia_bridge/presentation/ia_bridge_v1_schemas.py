from pydantic import BaseModel
from typing import Any, Optional


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


class OcrHistoryItem(BaseModel):
    id: str
    filename: str
    page_count: int
    created_at: str


class OcrHistoryResponse(BaseModel):
    data: list[OcrHistoryItem]
    total: int
    page: int
    limit: int


class NlpHistoryItem(BaseModel):
    id: str
    filename: str
    texto: str
    duracion_seg: float
    entidades: list[dict[str, Any]]
    created_at: str


class NlpHistoryResponse(BaseModel):
    data: list[NlpHistoryItem]
    total: int
    page: int
    limit: int


class NlpDetailResponse(BaseModel):
    id: str
    filename: str
    texto: str
    duracion_seg: float
    entidades: list[dict[str, Any]]
    created_at: str


class PredictionHistoryItem(BaseModel):
    id: str
    filename: str
    class_id: int
    tipo_dano: str
    severidad: str
    confianza: float
    prob_dist: list[float]
    created_at: str


class PredictionHistoryResponse(BaseModel):
    data: list[PredictionHistoryItem]
    total: int
    page: int
    limit: int


class SupervisedHealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str
    num_classes: int
    class_names: list[str]


class UnsupervisedHealthResponse(BaseModel):
    status: str
    model_loaded: bool
    k_value: Optional[int] = None
