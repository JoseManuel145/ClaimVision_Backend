from fastapi import APIRouter, Depends, File, UploadFile, Form, Query, Request, HTTPException
from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.ia_bridge.application.predict_damage import PredictDamage
from src.modules.ia_bridge.application.predict_all_damage import PredictAllDamage
from src.modules.ia_bridge.application.extract_text import ExtractText
from src.modules.ia_bridge.application.extract_poliza_data import ExtractPolizaData
from src.modules.ia_bridge.application.extract_ine_data import ExtractIneData
from src.modules.ia_bridge.application.extract_and_validate_data import ExtractAndValidateData
from src.modules.ia_bridge.application.transcribe_audio import TranscribeAudio
from src.modules.ia_bridge.application.analyze_text import AnalyzeText
from src.modules.ia_bridge.application.get_ocr_history import GetOcrHistory
from src.modules.ia_bridge.application.get_nlp_history import GetNlpHistory
from src.modules.ia_bridge.application.get_nlp_detail import GetNlpDetail
from src.modules.ia_bridge.application.get_prediction_history import GetPredictionHistory
from src.modules.ia_bridge.application.get_cost_summary import GetCostSummary
from src.modules.ia_bridge.application.get_health import GetSupervisedHealth, GetUnsupervisedHealth
from src.modules.ia_bridge.presentation.ia_bridge_v1_schemas import (
    PredictResponse,
    OcrResponse,
    TranscribirResponse,
    AnalizarResponse,
    OcrHistoryResponse,
    NlpHistoryResponse,
    NlpDetailResponse,
    PredictionHistoryResponse,
    SupervisedHealthResponse,
    UnsupervisedHealthResponse,
    PredictAllResponse,
    ResumenRequest,
    ResumenResponse,
)
from src.modules.ia_bridge.presentation.dependencies import (
    predict_service,
    predict_all_service,
    ia_ocr_service,
    extract_poliza_service,
    extract_ine_service,
    extract_and_validate_service,
    transcribir_service,
    analizar_service,
    get_ocr_history_service,
    get_nlp_history_service,
    get_nlp_detail_service,
    get_prediction_history_service,
    get_cost_summary_service,
    get_supervised_health_service,
    get_unsupervised_health_service,
)

router = APIRouter()

get_cliente_o_ajustador = require_roles("Cliente", "Ajustador", "Operador_Aseguradora")
get_ajustador = require_roles("Ajustador", "Operador_Aseguradora")


@router.post("/predict", response_model=PredictResponse)
@router.post("/v2/predict", response_model=PredictResponse)
@router.post("/predict/v2", response_model=PredictResponse)
async def predict_damage(
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: PredictDamage = Depends(predict_service),
):
    image_bytes = await file.read()
    return await uc.execute(image_bytes, file.filename, file.content_type)


@router.post("/v2/predict-all", response_model=PredictAllResponse)
async def predict_all(
    files: list[UploadFile] = File(...),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: PredictAllDamage = Depends(predict_all_service),
):
    file_tuples = []
    for f in files:
        file_bytes = await f.read()
        file_tuples.append((f.filename, file_bytes, f.content_type))
    return await uc.execute(file_tuples)


@router.post("/v2/obtener-resumen", response_model=ResumenResponse)
async def obtener_resumen(
    body: ResumenRequest,
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: GetCostSummary = Depends(get_cost_summary_service),
):
    return await uc.execute([d.model_dump() for d in body.danos])


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
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: TranscribeAudio = Depends(transcribir_service),
):
    audio_bytes = await file.read()
    return await uc.execute(audio_bytes, file.filename, file.content_type)


@router.get("/nlp/transcribir/status/{job_id}")
async def transcribe_status(
    job_id: str,
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: TranscribeAudio = Depends(transcribir_service),
):
    return await uc.get_status(job_id)


@router.post("/nlp/analizar", response_model=AnalizarResponse)
async def analyze_text(
    request: Request,
    texto: str | None = Form(None),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: AnalyzeText = Depends(analizar_service),
):
    text_content = texto
    if not text_content:
        try:
            body = await request.json()
            if isinstance(body, dict):
                text_content = body.get("texto")
        except Exception:
            pass
    if not text_content:
        raise HTTPException(status_code=422, detail="Se requiere el campo 'texto' (Form-data o JSON body).")
    return await uc.execute(text_content)


@router.get("/ocr/history", response_model=OcrHistoryResponse)
async def ocr_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: GetOcrHistory = Depends(get_ocr_history_service),
):
    return await uc.execute(page, limit)


@router.get("/nlp/history", response_model=NlpHistoryResponse)
async def nlp_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: GetNlpHistory = Depends(get_nlp_history_service),
):
    return await uc.execute(page, limit)


@router.get("/nlp/{job_id}", response_model=NlpDetailResponse)
async def nlp_detail(
    job_id: str,
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: GetNlpDetail = Depends(get_nlp_detail_service),
):
    return await uc.execute(job_id)


@router.get("/predict/history", response_model=PredictionHistoryResponse)
@router.get("/v2/history", response_model=PredictionHistoryResponse)
@router.get("/predict/v2/history", response_model=PredictionHistoryResponse)
async def prediction_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: AuthenticatedUser = Depends(get_cliente_o_ajustador),
    uc: GetPredictionHistory = Depends(get_prediction_history_service),
):
    return await uc.execute(page, limit)


@router.get("/predict/health", response_model=SupervisedHealthResponse)
@router.get("/v2/health", response_model=SupervisedHealthResponse)
@router.get("/predict/v2/health", response_model=SupervisedHealthResponse)
async def supervised_health(
    uc: GetSupervisedHealth = Depends(get_supervised_health_service),
):
    return await uc.execute()


@router.get("/unsupervised/health", response_model=UnsupervisedHealthResponse)
async def unsupervised_health(
    uc: GetUnsupervisedHealth = Depends(get_unsupervised_health_service),
):
    return await uc.execute()
