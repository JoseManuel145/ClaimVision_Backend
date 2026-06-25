from fastapi import APIRouter, Depends, status, UploadFile, File
from src.modules.siniestro.presentation.siniestros.siniestro_dto import SiniestroInicializarDTO, SiniestroResponseDTO, ImagenSiniestroResponseDTO, SiniestroUpdateDTO
from src.modules.siniestro.presentation.siniestros.siniestro_dependencies import (
    inicializar_siniestro_service,
    subir_imagen_siniestro_service,
    editar_siniestro_service
)
from src.core.security import get_current_user

router = APIRouter(tags=["Siniestros"])

@router.post("/inicializar", response_model=SiniestroResponseDTO, status_code=status.HTTP_201_CREATED)
def inicializar_siniestro(
    dto: SiniestroInicializarDTO,
    user=Depends(get_current_user),
    uc=Depends(inicializar_siniestro_service)
):
    # El usuario debe ser cliente para inicializar. (Podría agregarse validación de rol)
    return uc.execute(cliente_id=user.usuario_id, aseguradora_id=user.aseguradora_id, dto=dto)

@router.post("/{id}/imagenes", response_model=ImagenSiniestroResponseDTO, status_code=status.HTTP_201_CREATED)
async def subir_imagen(
    id: str,
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    uc=Depends(subir_imagen_siniestro_service)
):
    file_bytes = await file.read()
    return uc.execute(
        siniestro_id=id, 
        file_bytes=file_bytes, 
        filename=file.filename, 
        content_type=file.content_type
    )

@router.put("/{id}", response_model=SiniestroResponseDTO, status_code=status.HTTP_200_OK)
def editar_siniestro(
    id: str,
    dto: SiniestroUpdateDTO,
    user=Depends(get_current_user),
    uc=Depends(editar_siniestro_service)
):
    return uc.execute(siniestro_id=id, usuario_id=user.usuario_id, rol=user.rol, dto=dto)
