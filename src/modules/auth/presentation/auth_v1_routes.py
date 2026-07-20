from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.core.security import get_current_user
from src.core.rate_limit import limiter
from src.modules.auth.domain.models import AuthenticatedUser
from src.modules.auth.presentation import dependencies as deps
from src.modules.auth.presentation.schemas import (
    ConsentRequestDTO,
    LoginRequestDTO,
    LoginResponseDTO,
    UserRegister,
    RecoveryRequestDTO,
    RecoveryVerifyDTO,
    RecoveryResetDTO,
    ChangePasswordRequest,
    ChangePasswordWithCodeRequest,
    DeviceTokenRequestDTO,
)
from src.modules.auth.application.login_user import LoginUser
from src.modules.auth.application.register_user import RegisterUser
from src.modules.auth.application.generate_code import GenerateRecoveryCode
from src.modules.auth.application.send_recovery_code import SendRecoveryCode
from src.modules.auth.application.verify_code import VerifyRecoveryCode
from src.modules.auth.application.verify_user import VerifyUser
from src.modules.auth.application.reset_password import ResetPassword
from src.modules.auth.application.confirm_consent import ConfirmConsent
from src.modules.auth.application.change_password import ChangePassword
from src.modules.auth.application.request_password_change_code import RequestPasswordChangeCode
from src.modules.auth.application.change_password_with_code import ChangePasswordWithCode
from src.modules.auth.application.register_device_token import RegisterDeviceToken
from src.modules.auth.application.delete_device_token import DeleteDeviceToken
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository

router = APIRouter()




@router.post("/register", response_model=LoginResponseDTO, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
async def register(
    request: Request,
    data: UserRegister,
    usecase: RegisterUser = Depends(deps.register_user_service),
):
    return await usecase.execute(data)


@router.post("/login", response_model=LoginResponseDTO, status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(
    request: Request,
    data: LoginRequestDTO,
    usecase: LoginUser = Depends(deps.login_user_service),
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
@limiter.limit("3/minute")
async def request_recovery(
    request: Request,
    data: RecoveryRequestDTO,
    generate_uc: GenerateRecoveryCode = Depends(deps.generate_recovery_code_service),
    send_uc: SendRecoveryCode = Depends(deps.send_recovery_code_service),
):
    try:
        code = await generate_uc.execute(data.email)
        return await send_uc.execute(data.email, code)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))


@router.post("/recovery/verify", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def verify_code(
    request: Request,
    data: RecoveryVerifyDTO,
    usecase_code: VerifyRecoveryCode = Depends(deps.verify_recovery_code_service),
    usecase_auth: VerifyUser = Depends(deps.verify_user_service),
    auth_repo: AuthRepository = Depends(deps.get_auth_repo_service),
):
    target_id = data.usuario_id
    if not target_id and data.email:
        user = auth_repo.get_by_email(data.email)
        if user:
            target_id = user.usuario_id

    if not target_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se requiere usuario_id o email.")

    if await usecase_code.execute(target_id, data.code):
        return await usecase_auth.execute(target_id)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código inválido o expirado.")


@router.post("/recovery/reset", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def reset_password(
    request: Request,
    data: RecoveryResetDTO,
    usecase_verify: VerifyRecoveryCode = Depends(deps.verify_recovery_code_service),
    usecase_reset: ResetPassword = Depends(deps.reset_password_service),
    auth_repo: AuthRepository = Depends(deps.get_auth_repo_service),
):
    target_id = data.usuario_id
    if not target_id and data.email:
        user = auth_repo.get_by_email(data.email)
        if user:
            target_id = user.usuario_id

    if not target_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se requiere usuario_id o email.")

    if not await usecase_verify.execute(target_id, data.code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Código inválido o expirado.")
    return await usecase_reset.execute(target_id, data.new_password)



@router.post("/consentimiento", status_code=status.HTTP_200_OK)
async def submit_consentimiento(
    data: ConsentRequestDTO,
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: ConfirmConsent = Depends(deps.confirm_consent_service),
):
    try:
        usecase.execute(usuario_id=user.usuario_id, data=data)
        return {"message": "Consentimiento registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/password", status_code=status.HTTP_200_OK)
async def change_password(
    data: ChangePasswordRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: ChangePassword = Depends(deps.change_password_service),
):
    try:
        await usecase.execute(user.usuario_id, data.old_password, data.new_password)
        return {"message": "Contraseña actualizada exitosamente"}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al cambiar contraseña")


@router.post("/password/request-code", status_code=status.HTTP_200_OK)
async def request_password_change_code(
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: RequestPasswordChangeCode = Depends(deps.request_password_change_code_service),
):
    try:
        await usecase.execute(user.usuario_id)
        return {"message": "Código de verificación enviado a tu correo"}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al enviar código de verificación")


@router.post("/password/verify", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
async def change_password_with_code(
    request: Request,
    data: ChangePasswordWithCodeRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: ChangePasswordWithCode = Depends(deps.change_password_with_code_service),
):
    try:
        await usecase.execute(user.usuario_id, data.code, data.new_password)
        return {"message": "Contraseña actualizada exitosamente"}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al cambiar contraseña")


@router.post("/device-token", status_code=status.HTTP_201_CREATED)
def register_device_token(
    data: DeviceTokenRequestDTO,
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: RegisterDeviceToken = Depends(deps.register_device_token_service),
):
    usecase.execute(user.usuario_id, data.token)
    return {"ok": True}


@router.delete("/device-token", status_code=status.HTTP_204_NO_CONTENT)
def delete_device_token(
    data: DeviceTokenRequestDTO,
    user: AuthenticatedUser = Depends(get_current_user),
    usecase: DeleteDeviceToken = Depends(deps.delete_device_token_service),
):
    usecase.execute(user.usuario_id, data.token)
