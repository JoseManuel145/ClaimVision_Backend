from src.modules.auth.domain.models import TokenPayload
from src.modules.auth.domain.ports import TokenPort


class VerifyToken:

    def __init__(self, token_service: TokenPort):
        self.token_service = token_service

    async def execute(self, token: str) -> TokenPayload:
        return self.token_service.verify(token)
