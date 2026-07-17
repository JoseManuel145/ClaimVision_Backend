from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.taller_checker_port import TallerCheckerPort
from src.shared.domain.models import EstatusSiniestro
from src.shared.infra.messaging.siniestro_notifier import SiniestroNotifier
from src.core.exceptions import NotFoundError, BusinessRuleError

class EnviarTaller:
    def __init__(self, repo: SiniestroRepositoryPort, taller_checker: TallerCheckerPort, notifier: SiniestroNotifier | None = None):
        self.repo = repo
        self.taller_checker = taller_checker
        self.notifier = notifier

    def execute(self, siniestro_id: str, taller_id: str, aseguradora_id: str) -> SiniestroModel:
        siniestro = self.repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        
        if siniestro.aseguradora_id != aseguradora_id:
            raise BusinessRuleError("El siniestro no pertenece a la aseguradora actual")
            
        if not self.taller_checker.existe(taller_id):
            raise NotFoundError("Taller no encontrado o no válido")
            
        if siniestro.estatus != EstatusSiniestro.PERITAJE_VALIDADO.value:
            raise BusinessRuleError(f"No se puede enviar a taller un siniestro en estado {siniestro.estatus}. Debe tener peritaje validado.")

        siniestro.taller_id = taller_id
        siniestro.estatus = EstatusSiniestro.ASIGNADO_A_TALLER.value
        
        resultado = self.repo.update(siniestro)

        if self.notifier:
            self.notifier.notify_status_change(
                estatus=resultado.estatus,
                siniestro_id=resultado.id,
                cliente_id=resultado.cliente_id,
            )

        return resultado
