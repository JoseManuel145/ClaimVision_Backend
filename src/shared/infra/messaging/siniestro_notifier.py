from src.shared.domain.ports.messaging_port import MessagingPort
from src.shared.domain.ports.device_token_port import DeviceTokenPort
from src.shared.infra.events.sse_manager import sse_manager
from src.core.logging import get_logger

logger = get_logger("notification")



NOTIFICACIONES_SINIESTRO: dict[str, dict[str, dict[str, str]]] = {
    "Asignado_A_Ajustador": {
        "cliente": {
            "title": "Siniestro en revisión",
            "body": "Tu siniestro está siendo revisado por un ajustador.",
        },
        "ajustador": {
            "title": "Nuevo siniestro asignado",
            "body": "Se te ha asignado un nuevo siniestro para inspeccionar.",
        },
    },
    "Peritaje_Validado": {
        "cliente": {
            "title": "Peritaje completado",
            "body": "El peritaje de tu siniestro ha sido validado exitosamente.",
        },
    },
    "Asignado_A_Taller": {
        "cliente": {
            "title": "Siniestro en taller",
            "body": "Tu vehículo fue llevado al taller para reparación.",
        },
    },
    "Trabajo_Concluido": {
        "cliente": {
            "title": "Reparación concluida",
            "body": "El trabajo de reparación de tu vehículo ha sido concluido.",
        },
    },
    "Listo_Para_Entrega": {
        "cliente": {
            "title": "Vehículo listo para entrega",
            "body": "Tu vehículo está listo para ser recogido en el taller.",
        },
    },
    "Entregado": {
        "cliente": {
            "title": "Siniestro entregado",
            "body": "Tu siniestro ha sido marcado como entregado.",
        },
    },
}


class SiniestroNotifier:
    def __init__(self, messaging_service: MessagingPort, token_repo: DeviceTokenPort):
        self.fcm = messaging_service
        self.token_repo = token_repo

    def _send_to_user(self, user_id: str, title: str, body: str, data: dict[str, str]) -> None:
        tokens = self.token_repo.get_by_user(user_id)
        for device_token in tokens:
            try:
                self.fcm.send(
                    token=device_token.token,
                    title=title,
                    body=body,
                    data=data,
                )
            except Exception:
                logger.warning(f"Error al enviar notificación FCM al token {device_token.token[:20]}..., eliminando token inválido.")
                try:
                    self.token_repo.delete(device_token.token)
                except Exception:
                    pass

    def notify_status_change(
        self,
        estatus: str,
        siniestro_id: str,
        cliente_id: str | None = None,
        ajustador_id: str | None = None,
    ) -> None:
        # Emitir evento SSE siempre para la actualización en tiempo real del frontend
        sse_payload = {
            "entity": "siniestro",
            "action": "STATUS_CHANGE",
            "siniestro_id": siniestro_id,
            "estatus": estatus,
            "cliente_id": cliente_id,
            "ajustador_id": ajustador_id,
        }
        sse_manager.publish_event_sync(event="siniestro_updated", data=sse_payload)
        if cliente_id:
            sse_manager.publish_event_sync(event="siniestro_updated", data=sse_payload, target_user_id=cliente_id)
        if ajustador_id:
            sse_manager.publish_event_sync(event="siniestro_updated", data=sse_payload, target_user_id=ajustador_id)

        config = NOTIFICACIONES_SINIESTRO.get(estatus)
        if not config:
            return

        data_payload = {"type": "STATUS_CHANGE", "estatus": estatus, "siniestro_id": siniestro_id}

        if cliente_id and "cliente" in config:
            self._send_to_user(
                user_id=cliente_id,
                title=config["cliente"]["title"],
                body=config["cliente"]["body"],
                data=data_payload,
            )

        if ajustador_id and "ajustador" in config:
            self._send_to_user(
                user_id=ajustador_id,
                title=config["ajustador"]["title"],
                body=config["ajustador"]["body"],
                data=data_payload,
            )

