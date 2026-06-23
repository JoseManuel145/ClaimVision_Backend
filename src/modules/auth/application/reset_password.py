from src.modules.auth.domain.ports import AuthPort, PasswordPort


class ResetPassword:

    def __init__(self,repo: AuthPort, password_repo: PasswordPort):
        self.auth_repo = repo
        self.password_repo = password_repo

    async def execute(self, user_id: str, password: str):
        hash = self.password_repo.hash(password)
        return self.auth_repo.update_password(user_id, hash)