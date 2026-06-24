from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives.twofactor import InvalidToken
from jose import jwt, JWTError

from src.modules.auth.domain.models import TokenPayload
from src.modules.auth.domain.ports import TokenPort
from src.core.config import settings


class JwtTokenService(TokenPort):
    def __init__(self):
        pass

    def generate(self, payload: TokenPayload) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.TIME_MINUTES
        )

        to_encode = {
            "usuario_id": payload.usuario_id,
            "email": payload.email,
            "rol": payload.rol,
            "aseguradora_id": payload.aseguradora_id,
            "exp": expire,
        }

        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def verify(self, token: str) -> TokenPayload:
        try:
            decoded = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            return TokenPayload(
                usuario_id=decoded["usuario_id"],
                email=decoded["email"],
                rol=decoded["rol"],
                aseguradora_id=decoded.get("aseguradora_id"),
                exp=decoded["exp"],
            )
        except JWTError:
            raise InvalidToken()