from src.modules.auth.domain.models import AuthenticatedUser
from src.core.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr

from src.modules.auth.presentation.dependencies import (
    login_user_service,
    register_user_service,
    generate_recovery_code_service,
    send_recovery_code_service,
    verify_recovery_code_service,
    reset_password_service,
    verify_user_service,
    confirm_consent_service
)

from src.modules.auth.presentation.schemas import (
    UserRegister,
    LoginRequestDTO,
    LoginResponseDTO,
    ConsentRequestDTO
)

router = APIRouter()


@router.post("/register", response_model=LoginResponseDTO, status_code=status.HTTP_201_CREATED)
async def register(
        data: UserRegister,
        usecase=Depends(register_user_service),
):
    return await usecase.execute(
        data
    )


@router.post("/login", response_model=LoginResponseDTO, status_code=status.HTTP_200_OK)
async def login(
        data: LoginRequestDTO,
        usecase=Depends(login_user_service),
):
    try:
        return await usecase.execute(data.email, data.password)
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ve))


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(
        user: AuthenticatedUser = Depends(get_current_user),
):
    return user


@router.post("/recovery/request", status_code=status.HTTP_200_OK)
async def request_recovery(
        email: EmailStr,
        generate_uc=Depends(generate_recovery_code_service),
        send_uc=Depends(send_recovery_code_service),
):
    code = await generate_uc.execute(email)
    return await send_uc.execute(email, code)


@router.post("/recovery/verify", status_code=status.HTTP_200_OK)
async def verify_code(
        usuario_id: str,
        code: str,
        usecase_code=Depends(verify_recovery_code_service),
        usecase_auth=Depends(verify_user_service)
):
    if await usecase_code.execute(usuario_id, code):
        return await usecase_auth.execute(usuario_id)
    return None


@router.post("/recovery/reset", status_code=status.HTTP_200_OK)
async def reset_password(
        usuario_id: str,
        new_password: str,
        usecase=Depends(reset_password_service),
):
    return await usecase.execute(usuario_id, new_password)


@router.post("/consentimiento", status_code=status.HTTP_200_OK)
async def submit_consentimiento(
    data: ConsentRequestDTO,
    user: AuthenticatedUser = Depends(get_current_user),
    usecase = Depends(confirm_consent_service)
):
    try:
        usecase.execute(
            usuario_id=user.usuario_id,
            aviso_privacidad=data.aviso_privacidad,
            biometria=data.biometria,
            transferencia_talleres=data.transferencia_talleres
        )
        return {"message": "Consentimiento registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
