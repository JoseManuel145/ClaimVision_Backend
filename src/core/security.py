from fastapi import status
from fastapi import HTTPException
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.modules.auth.infra.jwt.token_service import JwtTokenService
from src.modules.auth.domain.models import AuthenticatedUser
from src.core.exceptions import UnauthorizedError

security_scheme = HTTPBearer()

def get_current_user(
    token_service: JwtTokenService = Depends(),
    auth_header: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> AuthenticatedUser:
    """
    Dependencia para obtener el usuario autenticado.
    Lanza UnauthorizedError si las credenciales son inválidas.
    """
    if auth_header is None:
        raise UnauthorizedError("No se proporcionó token de autorización")
    try:
        payload = token_service.verify(auth_header.credentials)
        return AuthenticatedUser(
            usuario_id=payload.usuario_id,
            email=payload.email,
            rol=payload.rol,
            aseguradora_id=payload.aseguradora_id
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas o expiradas",
            headers={"WWW-Authenticate": "Bearer"},
        )
