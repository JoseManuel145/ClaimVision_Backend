from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.shared.domain.models import EstatusSiniestro
from src.shared.infra.messaging.siniestro_notifier import SiniestroNotifier
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel

class ConfirmarPeritaje:
    def __init__(self, siniestro_repo: SiniestroRepositoryPort, peritaje_repo: PeritajeAjustadorRepositoryPort, notifier: SiniestroNotifier | None = None):
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo
        self.notifier = notifier

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

        resultado = self.siniestro_repo.update_estatus(siniestro_id, EstatusSiniestro.PERITAJE_VALIDADO.value)

        if self.notifier:
            self.notifier.notify_status_change(
                estatus=resultado.estatus,
                siniestro_id=resultado.id,
                cliente_id=resultado.cliente_id,
            )

        return resultado
