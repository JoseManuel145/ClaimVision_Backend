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
    Admite distribución Pub/Sub con Redis para despliegues multi-worker.
    """

    def __init__(self):
        self._subscriptions: Dict[str, ClientSubscription] = {}
        self._counter: int = 0
        self._redis_client = None
        self._pubsub_task: Optional[asyncio.Task] = None

    async def init_redis(self, redis_url: str):
        """Inicializa la conexión con Redis para Pub/Sub si redis_url está presente."""
        if not redis_url:
            logger.info("REDIS_URL no configurada. SSE funcionará en modo in-memory local.")
            return
        try:
            import redis.asyncio as aioredis
            self._redis_client = aioredis.from_url(redis_url, decode_responses=True)
            pubsub = self._redis_client.pubsub()
            await pubsub.subscribe("sse:events")
            self._pubsub_task = asyncio.create_task(self._redis_listener(pubsub))
            logger.info(f"Conexión Redis Pub/Sub inicializada para SSE ({redis_url})")
        except Exception as e:
            logger.warning(f"No se pudo conectar a Redis ({e}). SSE operará en modo in-memory local.")
            self._redis_client = None

    async def close_redis(self):
        """Cierra las conexiones y tareas asociadas a Redis."""
        if self._pubsub_task:
            self._pubsub_task.cancel()
            self._pubsub_task = None
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None

    async def _redis_listener(self, pubsub):
        """Escucha eventos publicados en la canal de Redis 'sse:events' y los distribuye localmente."""
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    payload = json.loads(message["data"])
                    await self._distribute_local(
                        event=payload["event"],
                        data=payload["data"],
                        target_user_id=payload.get("target_user_id"),
                        target_aseguradora_id=payload.get("target_aseguradora_id"),
                        target_role=payload.get("target_role"),
                        event_id=payload.get("event_id"),
                    )
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error en listener de Redis Pub/Sub SSE: {e}")

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
        Publica un evento a las suscripciones activas.
        Si Redis está conectado, publica en el canal Redis 'sse:events' para que todos los workers lo reciban.
        De lo contrario, distribuye directamente en la memoria local.
        """
        payload = {
            "event": event,
            "data": data,
            "target_user_id": target_user_id,
            "target_aseguradora_id": target_aseguradora_id,
            "target_role": target_role,
            "event_id": event_id,
        }

        if self._redis_client:
            try:
                await self._redis_client.publish("sse:events", json.dumps(payload, ensure_ascii=False))
                return
            except Exception as e:
                logger.warning(f"Fallo al publicar en Redis ({e}). Usando distribución local.")

        await self._distribute_local(
            event=event,
            data=data,
            target_user_id=target_user_id,
            target_aseguradora_id=target_aseguradora_id,
            target_role=target_role,
            event_id=event_id,
        )

    async def _distribute_local(
        self,
        event: str,
        data: Dict[str, Any],
        target_user_id: Optional[str] = None,
        target_aseguradora_id: Optional[str] = None,
        target_role: Optional[str] = None,
        event_id: Optional[str] = None,
    ):
        """Distribución local en memoria a las colas activas en este worker."""
        frame = self.format_sse_frame(event=event, data=data, event_id=event_id)
        dead_queues: List[str] = []

        for queue_id, sub in list(self._subscriptions.items()):
            # Filtrado por usuario específico
            if target_user_id and sub.user_id != target_user_id:
                continue

            # Filtrado por aseguradora (Administrador_Global puede recibir todo)
            if target_aseguradora_id and sub.role != "Administrador_Global":
                if sub.aseguradora_id != target_aseguradora_id:
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

