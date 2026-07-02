"""Fakes del módulo Cliente."""
from datetime import date, datetime, timezone
from typing import Optional

from src.modules.cliente.domain.models import ClienteProfile


class FakeClienteChecker:
    def __init__(self, mapping: dict[str, str]):
        self.mapping = mapping

    def get_perfil_cliente_id_by_usuario(self, usuario_id: str) -> Optional[str]:
        return self.mapping.get(usuario_id)


class FakeClienteRepo:
    def __init__(self, profile: ClienteProfile):
        self.profile = profile

    def get_by_usuario_id(self, usuario_id: str) -> Optional[ClienteProfile]:
        return self.profile if self.profile and self.profile.usuario_id == usuario_id else None

    def update(self, profile: ClienteProfile) -> ClienteProfile:
        self.profile = profile
        return profile


class FakeOcrService:
    def __init__(self, resultado: Optional[dict] = None):
        self.resultado = resultado or {
            "numero_poliza": "POL-999",
            "vigencia_poliza": "2030-12-31",
            "curp_rfc": "CURP123456XYZ",
        }

    async def execute(self, cedula_bytes: bytes, poliza_bytes: bytes) -> dict:
        return self.resultado


def default_cliente_profile() -> ClienteProfile:
    return ClienteProfile(
        id="perfil-1",
        usuario_id="user-1",
        numero_poliza="POL-123",
        vigencia_poliza=date(2030, 1, 1),
        curp_rfc_cifrado="cifrado",
        consentimiento_aviso_privacidad=True,
        consentimiento_biometria=False,
        autoriza_transferencia_talleres=False,
        fecha_consentimiento=datetime.now(timezone.utc),
    )
