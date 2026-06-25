from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel

class ConfirmarPeritaje:
    def __init__(self, siniestro_repo: SiniestroRepositoryPort, peritaje_repo: PeritajeAjustadorRepositoryPort):
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo

    async def execute(self, ajustador_id: str, siniestro_id: str) -> SiniestroModel:
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise ValueError("Siniestro no encontrado")
        
        if siniestro.ajustador_id != ajustador_id:
            raise PermissionError("No tienes permisos para modificar este siniestro")

        if siniestro.estatus in [EstatusSiniestro.PERITAJE_VALIDADO.value, EstatusSiniestro.ASIGNADO_A_TALLER.value, EstatusSiniestro.TRABAJO_CONCLUIDO.value, EstatusSiniestro.LISTO_PARA_ENTREGA.value, EstatusSiniestro.ENTREGADO.value]:
            raise ValueError("El siniestro ya fue validado")

        peritaje = self.peritaje_repo.obtener_peritaje_por_siniestro(siniestro_id)
        if not peritaje:
            raise ValueError("No se puede confirmar porque no hay un peritaje guardado")

        if not peritaje.firma_digital_ajustador:
            raise ValueError("El peritaje no tiene firma digital del ajustador")

        return self.siniestro_repo.update_estatus(siniestro_id, EstatusSiniestro.PERITAJE_VALIDADO.value)
