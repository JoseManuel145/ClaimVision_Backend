from src.modules.ajustador.application._helpers import resolver_ajustador_id
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.aseguradora.domain.ports.ajustador_repository_port import AjustadorRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.core.exceptions import NotFoundError, ForbiddenError, BusinessRuleError

_ESTADOS_BLOQUEADOS = {
    EstatusSiniestro.PERITAJE_VALIDADO.value,
    EstatusSiniestro.ASIGNADO_A_TALLER.value,
    EstatusSiniestro.TRABAJO_CONCLUIDO.value,
    EstatusSiniestro.LISTO_PARA_ENTREGA.value,
    EstatusSiniestro.ENTREGADO.value,
}


class _PeritajeEditorBase:
    def __init__(
        self,
        ajustador_repo: AjustadorRepositoryPort,
        siniestro_repo: SiniestroRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
    ):
        self.ajustador_repo = ajustador_repo
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo

    def _cargar_editable(self, usuario_id: str, peritaje_id: str) -> PeritajeAjustadorModel:
        ajustador_id = resolver_ajustador_id(self.ajustador_repo, usuario_id)
        peritaje = self.peritaje_repo.obtener_por_id(peritaje_id)
        if not peritaje:
            raise NotFoundError("Peritaje no encontrado")
        if peritaje.ajustador_id != ajustador_id:
            raise ForbiddenError("Este peritaje no pertenece al ajustador autenticado.")
        siniestro = self.siniestro_repo.get_by_id(peritaje.siniestro_id)
        if siniestro and siniestro.estatus in _ESTADOS_BLOQUEADOS:
            raise BusinessRuleError("El peritaje ya fue validado y no puede editarse.")
        return peritaje
