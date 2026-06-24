from src.modules.aseguradora.domain.models.siniestro_model import SiniestroModel
from src.modules.aseguradora.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.core.exceptions import NotFoundError, BusinessRuleError

class AutorizarEntrega:
    def __init__(self, repo: SiniestroRepositoryPort):
        self.repo = repo

    def execute(self, siniestro_id: str, aseguradora_id: str) -> SiniestroModel:
        siniestro = self.repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        
        if siniestro.aseguradora_id != aseguradora_id:
            raise BusinessRuleError("El siniestro no pertenece a la aseguradora actual")
            
        if siniestro.estatus != EstatusSiniestro.TRABAJO_CONCLUIDO.value:
            raise BusinessRuleError(f"No se puede autorizar entrega si el trabajo no ha concluido (estado actual: {siniestro.estatus})")

        siniestro.estatus = EstatusSiniestro.LISTO_PARA_ENTREGA.value
        
        # Enviar notificación (Push/Correo electrónico) indicando recolección.
        
        return self.repo.update(siniestro)
