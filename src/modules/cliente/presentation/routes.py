from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from src.modules.auth.domain.models import AuthenticatedUser
from src.core.security import get_current_user
from src.modules.cliente.presentation.schemas import ConfirmDataRequestDTO
from src.modules.cliente.presentation.dependencies import process_ocr_service, confirm_data_service
from src.modules.cliente.application.process_ocr import ProcessOcr
from src.modules.cliente.application.confirm_data import ConfirmData

router = APIRouter()

@router.post("/onboarding/ocr")
async def ocr_extraction(
    cedula: UploadFile = File(...),
    poliza: UploadFile = File(...),
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: ProcessOcr = Depends(process_ocr_service)
):
    try:
        cedula_bytes = await cedula.read()
        poliza_bytes = await poliza.read()
        data = await usecase.execute(cedula_bytes, poliza_bytes)
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/onboarding/confirmar-datos")
async def confirmar_datos(
    data: ConfirmDataRequestDTO,
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: ConfirmData = Depends(confirm_data_service)
):
    try:
        usecase.execute(
            usuario_id=user.usuario_id,
            data=data
        )
        return {"message": "Datos de onboarding confirmados y guardados de forma segura."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
