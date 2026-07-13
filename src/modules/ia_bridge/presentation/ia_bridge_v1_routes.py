from fastapi import APIRouter, Depends, File, UploadFile, Form
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.ia_bridge.application.predict_damage import PredictDamage
from src.modules.ia_bridge.application.extract_text import ExtractText
from src.modules.ia_bridge.application.extract_poliza_data import ExtractPolizaData
from src.modules.ia_bridge.application.extract_ine_data import ExtractIneData
from src.modules.ia_bridge.application.extract_and_validate_data import ExtractAndValidateData
from src.modules.ia_bridge.application.transcribe_audio import TranscribeAudio
from src.modules.ia_bridge.application.analyze_text import AnalyzeText
from src.modules.ia_bridge.presentation.ia_bridge_v1_schemas import (
    PredictResponse,
    OcrResponse,
    TranscribirResponse,
    AnalizarResponse,
)
from src.modules.ia_bridge.presentation.dependencies import (
    predict_service,
    ia_ocr_service,
    extract_poliza_service,
    extract_ine_service,
    extract_and_validate_service,
    transcribir_service,
    analizar_service,
)

router = APIRouter()

get_cliente_o_ajustador = require_roles("Cliente", "Ajustador")
get_ajustador = require_roles("Ajustador")


@router.post("/predict", response_model=PredictResponse)
async def predict_damage(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: PredictDamage = Depends(predict_service),
):
    image_bytes = await file.read()
    return await uc.execute(image_bytes, file.filename, file.content_type)


@router.post("/ocr", response_model=OcrResponse)
async def extract_text(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: ExtractText = Depends(ia_ocr_service),
):
    pdf_bytes = await file.read()
    return await uc.execute(pdf_bytes, file.filename, file.content_type)


@router.post("/ocr/extract-poliza")
async def extract_poliza(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: ExtractPolizaData = Depends(extract_poliza_service),
):
    pdf_bytes = await file.read()
    return await uc.execute(pdf_bytes, file.filename)


@router.post("/ocr/extract-ine")
async def extract_ine(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: ExtractIneData = Depends(extract_ine_service),
):
    file_bytes = await file.read()
    return await uc.execute(file_bytes, file.filename, file.content_type)


@router.post("/ocr/extract-and-validate")
async def extract_and_validate(
    poliza: UploadFile = File(...),
    ine: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: ExtractAndValidateData = Depends(extract_and_validate_service),
):
    poliza_bytes = await poliza.read()
    ine_bytes = await ine.read()
    return await uc.execute(
        poliza_bytes,
        poliza.filename,
        ine_bytes,
        ine.filename,
        ine.content_type,
    )


@router.post("/nlp/transcribir", response_model=TranscribirResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: TranscribeAudio = Depends(transcribir_service),
):
    audio_bytes = await file.read()
    return await uc.execute(audio_bytes, file.filename, file.content_type)


@router.get("/nlp/transcribir/status/{job_id}")
async def transcribe_status(
    job_id: str,
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: TranscribeAudio = Depends(transcribir_service),
):
    return await uc.get_status(job_id)


@router.post("/nlp/analizar", response_model=AnalizarResponse)
async def analyze_text(
    texto: str = Form(...),
    user: AuthenticatedUser = Depends(get_ajustador),
    uc: AnalyzeText = Depends(analizar_service),
):
    return await uc.execute(texto)
