from src.modules.auth.domain.ports import EmailPort


class SendRecoveryCode:
    def __init__(self, repo: EmailPort):
        self.repo = repo

    async def execute(self, to_email: str, code: str):
        return self.repo.send_code(to_email, code)