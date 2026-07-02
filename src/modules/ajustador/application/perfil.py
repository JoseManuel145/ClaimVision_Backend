"""Casos de uso del ajustador: disponibilidad y geolocalización."""
from datetime import datetime

from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.core.exceptions import BusinessRuleError


def _mi_perfil(ajustador_repo: AjustadorRepositoryPort, usuario_id: str) -> AjustadorModel:
    ajustador = ajustador_repo.get_by_usuario_id(usuario_id)
    if not ajustador:
        raise BusinessRuleError("El usuario no tiene un perfil de ajustador.")
    return ajustador


class ActualizarDisponibilidad:
    def __init__(self, ajustador_repo: AjustadorRepositoryPort):
        self.ajustador_repo = ajustador_repo

    def execute(self, usuario_id: str, activo_para_servicio: bool) -> AjustadorModel:
        ajustador = _mi_perfil(self.ajustador_repo, usuario_id)
        ajustador.activo_para_servicio = activo_para_servicio
        ajustador.version += 1
        ajustador.updated_at = datetime.utcnow()
        return self.ajustador_repo.update(ajustador)


class ActualizarGeolocalizacion:
    def __init__(self, ajustador_repo: AjustadorRepositoryPort):
        self.ajustador_repo = ajustador_repo

    def execute(self, usuario_id: str, latitud: float, longitud: float) -> AjustadorModel:
        ajustador = _mi_perfil(self.ajustador_repo, usuario_id)
        ajustador.geolocalizacion_actual = (latitud, longitud)
        ajustador.version += 1
        ajustador.updated_at = datetime.utcnow()
        return self.ajustador_repo.update(ajustador)
