"""Fakes del módulo Ajustador."""
from datetime import datetime
from typing import Optional

from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel


class FakeAjustadorRepo:
    def __init__(self, mapping: dict[str, AjustadorModel]):
        self.by_usuario = mapping
        self.by_id = {a.id: a for a in mapping.values()}

    def get_by_usuario_id(self, usuario_id: str):
        return self.by_usuario.get(usuario_id)

    def get_by_id(self, id: str):
        return self.by_id.get(id)

    def update(self, ajustador: AjustadorModel) -> AjustadorModel:
        self.by_id[ajustador.id] = ajustador
        self.by_usuario[ajustador.usuario_id] = ajustador
        return ajustador


def default_ajustador(usuario_id="user-aj", ajustador_id="aj-profile-1") -> AjustadorModel:
    return AjustadorModel(
        id=ajustador_id,
        usuario_id=usuario_id,
        cedula_profesional="CED-001",
        geolocalizacion_actual=None,
        activo_para_servicio=True,
        version=1,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
