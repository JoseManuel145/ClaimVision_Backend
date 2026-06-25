from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.taller_checker_port import TallerCheckerPort
from src.shared.domain.models import EstatusSiniestro
from src.core.exceptions import NotFoundError, BusinessRuleError

class EnviarTaller:
    def __init__(self, repo: SiniestroRepositoryPort, taller_checker: TallerCheckerPort):
        self.repo = repo
        self.taller_checker = taller_checker

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
        
        # Lógica de "Disociación Legal de Datos LFPDPPP" se maneja en el envío al taller
        # al omitir nombre y teléfono del cliente (eso ocurre en la lectura por el taller).
        
        return self.repo.update(siniestro)
