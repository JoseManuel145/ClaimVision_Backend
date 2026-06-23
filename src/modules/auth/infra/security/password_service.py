from src.modules.auth.domain.ports import PasswordPort
from passlib.context import CryptContext
from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=settings.BCRYPT_ROUNDS)
class PasswordService(PasswordPort):
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify(self, plain: str, hash: str) -> bool:
        return pwd_context.verify(plain, hash)