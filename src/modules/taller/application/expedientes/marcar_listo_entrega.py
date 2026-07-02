from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.shared.domain.transitions import validar_transicion
from src.core.exceptions import NotFoundError, ForbiddenError


class MarcarListoEntrega:
    """§6 · Trabajo_Concluido → Listo_Para_Entrega."""

    def __init__(self, siniestro_repo: SiniestroRepositoryPort, perfil_taller_repo: PerfilTallerRepositoryPort):
        self.siniestro_repo = siniestro_repo
        self.perfil_taller_repo = perfil_taller_repo

    def execute(self, usuario_id: str, siniestro_id: str) -> SiniestroModel:
        taller_id = self.perfil_taller_repo.get_taller_id_by_usuario(usuario_id)
        if not taller_id:
            raise ForbiddenError("El usuario no tiene un perfil de taller asignado.")
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        if siniestro.taller_id != taller_id:
            raise ForbiddenError("Este expediente no está asignado a tu taller.")

        validar_transicion(siniestro.estatus, EstatusSiniestro.LISTO_PARA_ENTREGA.value)
        return self.siniestro_repo.update_estatus(siniestro_id, EstatusSiniestro.LISTO_PARA_ENTREGA.value)
