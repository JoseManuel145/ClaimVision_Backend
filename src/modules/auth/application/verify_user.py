from src.modules.auth.domain.ports import AuthPort

class VerifyUser:
    def __init__(self, repo: AuthPort):
        self.repo = repo

    async def execute(self, user_id: str):
        return self.repo.verify_user(user_id)