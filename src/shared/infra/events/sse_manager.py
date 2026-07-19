import asyncio
import json
from typing import Any, Dict, List, Optional, Tuple
from src.core.logging import get_logger

logger = get_logger("sse_manager")


class ClientSubscription:
    def __init__(self, queue_id: str, user_id: str, role: str, aseguradora_id: Optional[str] = None):
        self.queue_id = queue_id
        self.user_id = user_id
        self.role = role
        self.aseguradora_id = aseguradora_id
        self.queue: asyncio.Queue = asyncio.Queue()

    async def put(self, item: str):
        await self.queue.put(item)


class SSEManager:
    """
    Gestor centralizado de Server-Sent Events (SSE).
    Administra la lista de clientes conectados y distribuye eventos en tiempo real
    filtrados por usuario, aseguradora y rol.
    """

    def __init__(self):
        self._subscriptions: Dict[str, ClientSubscription] = {}
        self._counter: int = 0

    def format_sse_frame(self, event: str, data: Dict[str, Any], event_id: Optional[str] = None) -> str:
        """Formatea un evento conforme al estándar SSE (text/event-stream)."""
        lines = []
        if event_id:
            lines.append(f"id: {event_id}")
        lines.append(f"event: {event}")
        lines.append(f"data: {json.dumps(data, ensure_ascii=False)}")
        lines.append("\n")  # Fin de la trama SSE
        return "\n".join(lines)

    def format_ping(self) -> str:
        """Formatea un comentario de ping (keep-alive)."""
        return ": ping\n\n"

    def subscribe(self, user_id: str, role: str, aseguradora_id: Optional[str] = None) -> Tuple[str, asyncio.Queue]:
        """Registra a un cliente y retorna (queue_id, asyncio.Queue)."""
        self._counter += 1
        queue_id = f"{user_id}_{self._counter}"
        sub = ClientSubscription(
            queue_id=queue_id,
            user_id=user_id,
            role=role,
            aseguradora_id=aseguradora_id,
        )
        self._subscriptions[queue_id] = sub
        logger.info(f"Cliente SSE suscrito: {queue_id} (rol={role}, aseguradora={aseguradora_id})")
        return queue_id, sub.queue

    def unsubscribe(self, queue_id: str):
        """Elimina la suscripción de un cliente."""
        if queue_id in self._subscriptions:
            del self._subscriptions[queue_id]
            logger.info(f"Cliente SSE desuscrito: {queue_id}")

    async def publish_event(
        self,
        event: str,
        data: Dict[str, Any],
        target_user_id: Optional[str] = None,
        target_aseguradora_id: Optional[str] = None,
        target_role: Optional[str] = None,
        event_id: Optional[str] = None,
    ):
        """
        Publica un evento a las suscripciones activas que coincidan con los criterios.
        Si no se especifican targets, se transmite a todas las conexiones de la aseguradora/rol relevante.
        """
        frame = self.format_sse_frame(event=event, data=data, event_id=event_id)
        dead_queues: List[str] = []

        for queue_id, sub in list(self._subscriptions.items()):
            # Filtrado por usuario específico
            if target_user_id and sub.user_id != target_user_id:
                continue

            # Filtrado por aseguradora (Administrador_Global puede recibir todo)
            if target_aseguradora_id and sub.role != "Administrador_Global":
                if sub.aseguradora_id and sub.aseguradora_id != target_aseguradora_id:
                    continue

            # Filtrado por rol
            if target_role and sub.role != target_role and sub.role != "Administrador_Global":
                continue

            try:
                await sub.put(frame)
            except Exception as e:
                logger.warning(f"Error al enviar evento SSE a {queue_id}: {e}")
                dead_queues.append(queue_id)

        for qid in dead_queues:
            self.unsubscribe(qid)

    def publish_event_sync(
        self,
        event: str,
        data: Dict[str, Any],
        target_user_id: Optional[str] = None,
        target_aseguradora_id: Optional[str] = None,
        target_role: Optional[str] = None,
        event_id: Optional[str] = None,
    ):
        """Versión sincrónica de publish_event para llamar desde servicios/use cases sincrónicos."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(
                self.publish_event(
                    event=event,
                    data=data,
                    target_user_id=target_user_id,
                    target_aseguradora_id=target_aseguradora_id,
                    target_role=target_role,
                    event_id=event_id,
                )
            )
        except RuntimeError:
            # Si no hay un loop corriendo en este thread, ejecutar en un loop nuevo temporal
            asyncio.run(
                self.publish_event(
                    event=event,
                    data=data,
                    target_user_id=target_user_id,
                    target_aseguradora_id=target_aseguradora_id,
                    target_role=target_role,
                    event_id=event_id,
                )
            )


# Instancia Singleton global para la aplicación
sse_manager = SSEManager()

