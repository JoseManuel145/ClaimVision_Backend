from src.core.database import get_session
from fastapi import Depends

# infra
from src.modules.auth.infra.db.repositories.recovery_repository import RecoveryCodeService
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.cliente.infra.db.repositories.cliente_repository import ClienteRepository
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.auth.infra.messaging.email_service import EmailService
from src.modules.auth.infra.jwt.token_service import JwtTokenService
from src.modules.auth.infra.db.repositories.login_attempt_repository import InMemoryLoginAttemptRepository

# Instancia global para mantener estado en memoria
in_memory_login_attempt_repo = InMemoryLoginAttemptRepository()

# usecases
from src.modules.auth.application import (
    VerifyToken,
    LoginUser,
    RegisterUser,
    GenerateRecoveryCode,
    ResetPassword,
    VerifyRecoveryCode,
    SendRecoveryCode,
    VerifyUser,
    ConfirmConsent
)
from src.modules.auth.application.change_password import ChangePassword
from src.modules.auth.application.request_password_change_code import RequestPasswordChangeCode
from src.modules.auth.application.change_password_with_code import ChangePasswordWithCode

def verify_token_service():
    token_service = JwtTokenService()
    return VerifyToken(token_service)

def register_user_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    password_service = PasswordService()
    token_service = JwtTokenService()
    return RegisterUser(repo, password_service, token_service)

def login_user_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    password_service = PasswordService()
    token_service = JwtTokenService()
    return LoginUser(repo, password_service, token_service, in_memory_login_attempt_repo)

def generate_recovery_code_service(session=Depends(get_session)):
    recovery_repo = RecoveryCodeService(session)
    user_repo = AuthRepository(session)
    return GenerateRecoveryCode(recovery_repo, user_repo)

def send_recovery_code_service():
    email_service = EmailService()
    return SendRecoveryCode(email_service)

def verify_recovery_code_service(session=Depends(get_session)):
    recovery_repo = RecoveryCodeService(session)
    return VerifyRecoveryCode(recovery_repo)

def reset_password_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    password_service = PasswordService()
    return ResetPassword(repo, password_service)

def verify_user_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    return VerifyUser(repo)

def confirm_consent_service(session=Depends(get_session)):
    auth_repo = AuthRepository(session)
    cliente_repo = ClienteRepository(session)
    return ConfirmConsent(cliente_repo, auth_repo)


def change_password_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    password_service = PasswordService()
    return ChangePassword(repo, password_service)


def request_password_change_code_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    recovery_repo = RecoveryCodeService(session)
    email_service = EmailService()
    return RequestPasswordChangeCode(repo, recovery_repo, email_service)


def change_password_with_code_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    password_service = PasswordService()
    recovery_repo = RecoveryCodeService(session)
    return ChangePasswordWithCode(repo, password_service, recovery_repo)
