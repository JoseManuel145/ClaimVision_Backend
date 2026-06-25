from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.ajustador_checker_port import AjustadorCheckerPort
from src.shared.domain.models import EstatusSiniestro
from src.core.exceptions import NotFoundError, BusinessRuleError

class AsignarAjustador:
    def __init__(self, repo: SiniestroRepositoryPort, ajustador_checker: AjustadorCheckerPort):
        self.repo = repo
        self.ajustador_checker = ajustador_checker

    def execute(self, siniestro_id: str, ajustador_id: str, aseguradora_id: str) -> SiniestroModel:
        siniestro = self.repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")
        
        if siniestro.aseguradora_id != aseguradora_id:
            raise BusinessRuleError("El siniestro no pertenece a la aseguradora actual")
            
        if not self.ajustador_checker.existe_y_activo(ajustador_id):
            raise NotFoundError("Ajustador no encontrado o inactivo")
            
        if siniestro.estatus != EstatusSiniestro.REPORTADO_PRELIMINAR.value:
            raise BusinessRuleError(f"No se puede asignar ajustador en estado {siniestro.estatus}")

        siniestro.ajustador_id = ajustador_id
        siniestro.estatus = EstatusSiniestro.ASIGNADO_A_AJUSTADOR.value
        return self.repo.update(siniestro)
