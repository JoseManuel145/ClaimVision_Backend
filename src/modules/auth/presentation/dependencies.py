from src.core.database import get_session
from fastapi import Depends

# infra
from src.modules.auth.infra.db.repositories.recovery_repository import RecoveryCodeService
from src.modules.auth.infra.db.repositories.auth_repository import AuthRepository
from src.modules.auth.infra.google.google_oauth_service import GoogleOAuthService
from src.modules.auth.infra.security.password_service import PasswordService
from src.modules.auth.infra.messaging.email_service import EmailService
from src.modules.auth.infra.jwt.token_service import JwtTokenService
from src.modules.auth.infra.db.repositories.login_attempt_repository import InMemoryLoginAttemptRepository

# Instancia global para mantener estado en memoria
in_memory_login_attempt_repo = InMemoryLoginAttemptRepository()

# usecases
from src.modules.auth.application import (
    VerifyToken,
    GetByGoogle,
    LoginUser,
    RegisterUser,
    GetGoogleAuthUrl,
    GenerateRecoveryCode,
    LoginWithGoogle,
    ResetPassword,
    VerifyRecoveryCode,
    SendRecoveryCode,
    VerifyUser
)

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

def login_with_google_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    google_service = GoogleOAuthService()
    token_service = JwtTokenService()
    return LoginWithGoogle(google_service, repo, token_service)

def get_by_google_service(session=Depends(get_session)):
    repo = AuthRepository(session)
    return GetByGoogle(repo)

def get_google_auth_url_service():
    google_service = GoogleOAuthService()
    return GetGoogleAuthUrl(google_service)

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