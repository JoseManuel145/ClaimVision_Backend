import os
import base64
from fastapi import status
from fastapi import HTTPException
from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.modules.auth.infra.jwt.token_service import JwtTokenService
from src.modules.auth.domain.models import AuthenticatedUser
from src.core.exceptions import UnauthorizedError
from src.core.config import settings
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

security_scheme = HTTPBearer()

def _get_aesgcm() -> AESGCM:
    key_bytes = base64.b64decode(settings.ENCRYPTION_KEY)
    return AESGCM(key_bytes)

def encrypt_aes256(plain_text: str) -> str:
    """Cifra un texto utilizando AES-256-GCM. Retorna string base64."""
    if not plain_text:
        return ""
    aesgcm = _get_aesgcm()
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, plain_text.encode('utf-8'), None)
    return base64.b64encode(nonce + encrypted).decode('utf-8')

def decrypt_aes256(cipher_text: str) -> str:
    """Descifra un texto cifrado con AES-256-GCM desde string base64."""
    if not cipher_text:
        return ""
    try:
        data = base64.b64decode(cipher_text.encode('utf-8'))
        nonce = data[:12]
        encrypted = data[12:]
        aesgcm = _get_aesgcm()
        decrypted = aesgcm.decrypt(nonce, encrypted, None)
        return decrypted.decode('utf-8')
    except Exception:
        return cipher_text # Fallback o podríamos levantar ValueError

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


def require_roles(*roles: str):
    """
    Factory de dependencia para RBAC. Devuelve una dependencia que valida que el
    usuario autenticado tenga uno de los `roles` permitidos (valores del enum
    `rol_usuario`). `Administrador_Global` siempre pasa (acceso global multi-tenant).

    Uso:
        get_cliente = require_roles("Cliente")
        @router.get(..., dependencies=[Depends(get_cliente)])
        # o para usar el usuario:
        def endpoint(user: AuthenticatedUser = Depends(get_cliente)): ...
    """
    allowed = set(roles)

    def _dependency(user: AuthenticatedUser = Depends(get_current_user)) -> AuthenticatedUser:
        if user.rol == "Administrador_Global" or user.rol in allowed:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acceso denegado. Rol requerido: {', '.join(sorted(allowed))}.",
        )

    return _dependency
