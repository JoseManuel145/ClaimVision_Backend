import hashlib
from datetime import datetime, timezone

from src.modules.auth.domain.ports import RecoveryCodePort


class VerifyRecoveryCode:

    def __init__(self, repo: RecoveryCodePort):
        self.repo = repo

    async def execute(self, user_id: str, input_code: str) -> bool:

        recovery = self.repo.get_by_user_id(user_id)

        if not recovery:
            return False

        if recovery.is_expired(datetime.now(timezone.utc)):
            self.repo.delete_by_user_id(user_id)
            return False

        hashed_input = hashlib.sha256(input_code.encode()).hexdigest()

        if hashed_input != recovery.code:
            return False

        self.repo.delete_by_user_id(user_id)
        return True
