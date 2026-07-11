from datetime import datetime

from src.modules.aseguradora.domain.models.ajustador_model import AjustadorModel
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.core.exceptions import BusinessRuleError


class ActualizarGeolocalizacion:
    def __init__(self, ajustador_repo: AjustadorRepositoryPort):
        self.ajustador_repo = ajustador_repo

    def execute(self, usuario_id: str, latitud: float, longitud: float) -> AjustadorModel:
        ajustador = self.ajustador_repo.get_by_usuario_id(usuario_id)
        if not ajustador:
            raise BusinessRuleError("El usuario no tiene un perfil de ajustador.")
        ajustador.geolocalizacion_actual = (latitud, longitud)
        ajustador.updated_at = datetime.utcnow()
        return self.ajustador_repo.update(ajustador)
