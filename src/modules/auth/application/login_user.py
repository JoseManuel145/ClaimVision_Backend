from src.modules.auth.domain.ports import AuthPort, PasswordPort, TokenPort, LoginAttemptPort
from src.modules.auth.domain.models import User, TokenPayload
from src.shared.domain.models import EstadoUsuario
from datetime import datetime, timedelta, timezone

class LoginUser:

    def __init__(
        self,
        auth_repo: AuthPort,
        password_port: PasswordPort,
        token_port: TokenPort,
        login_attempt_port: LoginAttemptPort,
    ):
        self.auth_repo = auth_repo
        self.password_port = password_port
        self.token_port = token_port
        self.login_attempt_port = login_attempt_port

    async def execute(self, email: str, password: str):
        if self.login_attempt_port.is_blocked(email):
            raise ValueError("Cuenta bloqueada temporalmente. Intente más tarde.")

        user = self.auth_repo.get_by_email(email)
        if not user:
            raise ValueError("Credenciales inválidas")

        if user.estado == EstadoUsuario.BLOQUEADO_ARCO.value:
            raise PermissionError("Acceso denegado: Cuenta bloqueada por ARCO")

        if not self.password_port.verify(password, user.password):
            attempts = self.login_attempt_port.record_failed_attempt(email)
            if attempts >= 5:
                raise ValueError("Demasiados intentos fallidos. Cuenta bloqueada temporalmente.")
            raise ValueError("Credenciales inválidas")

        self.login_attempt_port.reset_attempts(email)

        data = TokenPayload(
            usuario_id=user.usuario_id,
            email=user.email,
            rol=user.rol,
            aseguradora_id=user.aseguradora_id,
            exp=datetime.now(timezone.utc) + timedelta(hours=1),
        )
        token = self.token_port.generate(data)
        return {
            "token": token,
            "usuario_id": user.usuario_id,
            "email": user.email,
            "rol": user.rol,
            "aseguradora_id": user.aseguradora_id,
            "primer_cambio_password": user.primer_cambio_password,
        }