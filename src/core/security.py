import os
import base64
import logging
from fastapi import status
from fastapi import HTTPException
from typing import Optional

logger = logging.getLogger(__name__)

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.modules.auth.infra.jwt.token_service import JwtTokenService
from src.modules.auth.domain.models import AuthenticatedUser
from src.core.exceptions import UnauthorizedError
from src.core.config import settings
from nacl.secret import SecretBox
from nacl.utils import random as nacl_random
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

security_scheme = HTTPBearer()

XSALSA20_NONCE_SIZE = 24
AES_GCM_NONCE_SIZE = 12

def _get_xsalsa20_key() -> bytes:
    key_bytes = base64.b64decode(settings.ENCRYPTION_KEY)
    return key_bytes[:32]

def encrypt_xsalsa20(plain_text: str) -> str:
    """Cifra un texto utilizando XSalsa20-Poly1305 (NaCl). Retorna string base64."""
    if not plain_text:
        return ""
    key = _get_xsalsa20_key()
    box = SecretBox(key)
    nonce = nacl_random(XSALSA20_NONCE_SIZE)
    encrypted = box.encrypt(plain_text.encode('utf-8'), nonce)
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_xsalsa20(cipher_text: str) -> str:
    """Descifra un texto cifrado con XSalsa20-Poly1305 desde string base64."""
    if not cipher_text:
        return ""
    try:
        key = _get_xsalsa20_key()
        box = SecretBox(key)
        data = base64.b64decode(cipher_text.encode('utf-8'))
        decrypted = box.decrypt(data)
        return decrypted.decode('utf-8')
    except Exception:
        logger.warning("Fallo descifrado XSalsa20, intentando AES-GCM legacy: %s caracteres", len(cipher_text))
        return decrypt_aes256_legacy(cipher_text)

def decrypt_aes256_legacy(cipher_text: str) -> str:
    """Descifra datos legacy cifrados con AES-256-GCM (fallback)."""
    if not cipher_text:
        return ""
    try:
        key_bytes = base64.b64decode(settings.ENCRYPTION_KEY)
        aesgcm = AESGCM(key_bytes)
        data = base64.b64decode(cipher_text.encode('utf-8'))
        nonce = data[:AES_GCM_NONCE_SIZE]
        encrypted = data[AES_GCM_NONCE_SIZE:]
        decrypted = aesgcm.decrypt(nonce, encrypted, None)
        return decrypted.decode('utf-8')
    except Exception:
        logger.warning("Fallo descifrado AES-256 legacy, probablemente dato en plano: %s caracteres", len(cipher_text))
        return cipher_text

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
