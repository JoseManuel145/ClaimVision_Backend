from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.shared.infra.messaging.siniestro_notifier import SiniestroNotifier
from src.core.exceptions import NotFoundError, BusinessRuleError

class AutorizarEntrega:
    def __init__(self, repo: SiniestroRepositoryPort, notifier: SiniestroNotifier | None = None):
        self.repo = repo
        self.notifier = notifier

    def execute(self, siniestro_id: str, aseguradora_id: str) -> SiniestroModel:
        siniestro = self.repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        
        if siniestro.aseguradora_id != aseguradora_id:
            raise BusinessRuleError("El siniestro no pertenece a la aseguradora actual")
            
        if siniestro.estatus != EstatusSiniestro.TRABAJO_CONCLUIDO.value:
            raise BusinessRuleError(f"No se puede autorizar entrega si el trabajo no ha concluido (estado actual: {siniestro.estatus})")

        siniestro.estatus = EstatusSiniestro.LISTO_PARA_ENTREGA.value
        
        resultado = self.repo.update(siniestro)

        if self.notifier:
            self.notifier.notify_status_change(
                estatus=resultado.estatus,
                siniestro_id=resultado.id,
                cliente_id=resultado.cliente_id,
            )

        return resultado
