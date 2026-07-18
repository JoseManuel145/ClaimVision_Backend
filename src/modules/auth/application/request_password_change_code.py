from src.modules.auth.domain.ports import AuthPort, RecoveryCodePort, EmailPort
from src.modules.auth.domain.models import RecoveryCode
from datetime import datetime, timedelta, timezone
import hashlib
import secrets
import string


class RequestPasswordChangeCode:

    def __init__(self, auth_repo: AuthPort, recovery_repo: RecoveryCodePort, email_port: EmailPort):
        self.auth_repo = auth_repo
        self.recovery_repo = recovery_repo
        self.email_port = email_port

    async def execute(self, user_id: str):
        user = self.auth_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        plain_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        code_hash = hashlib.sha256(plain_code.encode()).hexdigest()

        self.recovery_repo.delete_by_user_id(user_id)

        recovery = RecoveryCode(
            id=None,
            usuario_id=user_id,
            code=code_hash,
            expires_at=expires_at,
        )
        self.recovery_repo.save(recovery)

        self.email_port.send_code(user.email, plain_code)
