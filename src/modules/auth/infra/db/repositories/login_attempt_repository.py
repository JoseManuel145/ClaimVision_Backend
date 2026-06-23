from datetime import datetime, timedelta, timezone
from src.modules.auth.domain.ports import LoginAttemptPort

class InMemoryLoginAttemptRepository(LoginAttemptPort):
    def __init__(self):
        # Almacena { 
        #     email: 
        #     {
        #         "attempts": int, 
        #         "blocked_until": datetime | None
        #     } 
        # }
        self._attempts = {}

    def record_failed_attempt(self, email: str) -> int:
        now = datetime.now(timezone.utc)
        record = self._attempts.get(email)

        if not record:
            self._attempts[email] = {"attempts": 1, "blocked_until": None}
            return 1

        if record["blocked_until"] and record["blocked_until"] > now:
            return record["attempts"]

        record["attempts"] += 1
        if record["attempts"] >= 5:
            record["blocked_until"] = now + timedelta(minutes=15)

        return record["attempts"]

    def is_blocked(self, email: str) -> bool:
        now = datetime.now(timezone.utc)
        record = self._attempts.get(email)
        if not record:
            return False

        if record["blocked_until"] and record["blocked_until"] > now:
            return True

        if record["blocked_until"] and record["blocked_until"] <= now:
            self.reset_attempts(email)
            return False

        return False

    def reset_attempts(self, email: str) -> None:
        if email in self._attempts:
            del self._attempts[email]
