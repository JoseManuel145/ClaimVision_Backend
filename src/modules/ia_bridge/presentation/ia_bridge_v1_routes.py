from fastapi import APIRouter, Depends, File, UploadFile, Form
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.ia_bridge.application.predict_damage import PredictDamage
from src.modules.ia_bridge.application.extract_text import ExtractText
from src.modules.ia_bridge.application.transcribe_audio import TranscribeAudio
from src.modules.ia_bridge.application.analyze_text import AnalyzeText
from src.modules.ia_bridge.presentation.dependencies import (
    predict_service,
    ia_ocr_service,
    transcribir_service,
    analizar_service,
)

router = APIRouter()

get_cliente_o_ajustador = require_roles("Cliente", "Ajustador")
get_ajustador = require_roles("Ajustador")


@router.post("/predict")
async def predict_damage(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: PredictDamage = Depends(predict_service),
):
    image_bytes = await file.read()
    return await uc.execute(image_bytes, file.filename)


@router.post("/ocr")
async def extract_text(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: ExtractText = Depends(ia_ocr_service),
):
    pdf_bytes = await file.read()
    return await uc.execute(pdf_bytes, file.filename)


@router.post("/nlp/transcribir")
async def transcribe_audio(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: TranscribeAudio = Depends(transcribir_service),
):
    audio_bytes = await file.read()
    return await uc.execute(audio_bytes, file.filename)


@router.get("/nlp/transcribir/status/{job_id}")
async def transcribe_status(
    job_id: str,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: TranscribeAudio = Depends(transcribir_service),
):
    return await uc.get_status(job_id)


@router.post("/nlp/analizar")
async def analyze_text(
    texto: str = Form(...),
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: AnalyzeText = Depends(analizar_service),
):
    return await uc.execute(texto)
