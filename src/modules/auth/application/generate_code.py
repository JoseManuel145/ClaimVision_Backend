from src.modules.auth.domain.ports import AuthPort
from src.modules.auth.domain.ports import RecoveryCodePort
from src.modules.auth.domain.models import RecoveryCode
from datetime import datetime, timedelta, timezone
import hashlib
import secrets
import string

class GenerateRecoveryCode:

    def __init__(self, repo: RecoveryCodePort, user_repo: AuthPort):
        self.repo = repo
        self.user_repo = user_repo

    async def execute(self, email: str) -> tuple[str, datetime]:

        user = self.user_repo.get_by_email(email)
        plain_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
        code_hash = hashlib.sha256(plain_code.encode()).hexdigest()

        self.repo.delete_by_user_id(user.usuario_id)

        recovery = RecoveryCode(
            id=None,
            usuario_id=user.usuario_id,
            code=code_hash,
            expires_at=expires_at
        )

        self.repo.save(recovery)

        return plain_code, expires_at
