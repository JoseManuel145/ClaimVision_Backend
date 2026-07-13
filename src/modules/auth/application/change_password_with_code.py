import hashlib
from datetime import datetime, timezone

from src.modules.auth.domain.ports import AuthPort, PasswordPort, RecoveryCodePort


class ChangePasswordWithCode:

    def __init__(self, auth_repo: AuthPort, password_port: PasswordPort, recovery_repo: RecoveryCodePort):
        self.auth_repo = auth_repo
        self.password_port = password_port
        self.recovery_repo = recovery_repo

    async def execute(self, user_id: str, code: str, new_password: str):
        user = self.auth_repo.get_by_id(user_id)
        if not user:
            raise ValueError("Usuario no encontrado")

        recovery = self.recovery_repo.get_by_user_id(user_id)
        if not recovery:
            raise ValueError("Código no encontrado. Solicite uno nuevo.")

        if recovery.is_expired(datetime.now(timezone.utc)):
            self.recovery_repo.delete_by_user_id(user_id)
            raise ValueError("El código ha expirado. Solicite uno nuevo.")

        hashed_input = hashlib.sha256(code.encode()).hexdigest()
        if hashed_input != recovery.code:
            raise ValueError("Código inválido.")

        self.recovery_repo.delete_by_user_id(user_id)

        new_hash = self.password_port.hash(new_password)
        self.auth_repo.update_password(user_id, new_hash)
