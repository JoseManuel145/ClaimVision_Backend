from fastapi import HTTPException
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.shared.domain.models import EstatusSiniestro, EstatusCotizacion
from src.shared.infra.messaging.siniestro_notifier import SiniestroNotifier

class ConcluirExpedienteUseCase:
    def __init__(
        self,
        siniestro_repo: SiniestroRepositoryPort,
        cotizacion_repo: CotizacionRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort,
        notifier: SiniestroNotifier | None = None,
    ):
        self.siniestro_repo = siniestro_repo
        self.cotizacion_repo = cotizacion_repo
        self.perfil_taller_repo = perfil_taller_repo
        self.notifier = notifier

    def execute(self, siniestro_id: str, usuario_id: str) -> None:
        taller_id = self.perfil_taller_repo.get_taller_id_by_usuario(usuario_id)
        if not taller_id:
            raise HTTPException(status_code=403, detail="El usuario no tiene un perfil de taller asignado.")
            
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise HTTPException(status_code=404, detail="Siniestro no encontrado.")
            
        if siniestro.taller_id != taller_id:
            raise HTTPException(status_code=403, detail="Este expediente no está asignado a tu taller.")
            
        cotizacion = self.cotizacion_repo.get_by_siniestro(siniestro_id)
        if not cotizacion or cotizacion.estatus != EstatusCotizacion.APROBADA.value:
            raise HTTPException(status_code=400, detail="No se puede concluir el trabajo sin una cotización aprobada.")
            
        resultado = self.siniestro_repo.update_estatus(siniestro_id, EstatusSiniestro.TRABAJO_CONCLUIDO.value)

        if self.notifier:
            self.notifier.notify_status_change(
                estatus=resultado.estatus,
                siniestro_id=resultado.id,
                cliente_id=resultado.cliente_id,
            )
