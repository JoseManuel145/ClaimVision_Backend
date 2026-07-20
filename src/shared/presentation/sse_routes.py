import asyncio
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import StreamingResponse

from src.core.security import get_current_user_sse
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.infra.events.sse_manager import sse_manager
from src.core.logging import get_logger

logger = get_logger("sse_routes")

router = APIRouter(prefix="/events", tags=["v1 · Events (SSE)"])


@router.get("/stream")
async def event_stream(
    request: Request,
    token: str | None = Query(None, description="JWT token opcional para clientes EventSource nativos"),
    user: AuthenticatedUser = Depends(get_current_user_sse),
):
    """
    §SSE · Endpoint de streaming en tiempo real (Server-Sent Events).
    Transmite eventos de actualización de siniestros, ajustadores, clientes, talleres y vehículos
    para refrescar los GETs del frontend en tiempo real.
    """
    queue_id, queue = sse_manager.subscribe(
        user_id=user.usuario_id,
        role=user.rol,
        aseguradora_id=user.aseguradora_id,
    )

    async def event_generator():
        # Enviar mensaje inicial de conexión establecida
        init_frame = sse_manager.format_sse_frame(
            event="connected",
            data={
                "message": "Conexión SSE establecida con éxito.",
                "user_id": user.usuario_id,
                "rol": user.rol,
            },
        )
        yield init_frame

        try:
            while True:
                if await request.is_disconnected():
                    logger.info(f"Cliente SSE desconectado: {queue_id}")
                    break

                try:
                    # Esperar evento durante 15 segundos antes de enviar keep-alive ping
                    message = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield message
                except asyncio.TimeoutError:
                    yield sse_manager.format_ping()
        except asyncio.CancelledError:
            logger.info(f"Conexión SSE cancelada para {queue_id}")
        finally:
            sse_manager.unsubscribe(queue_id)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Content-Encoding": "none",
        },
    )


@router.get("/stream/siniestro/{id}")
async def siniestro_event_stream(
    id: str,
    request: Request,
    token: str | None = Query(None, description="JWT token opcional para clientes EventSource nativos"),
    user: AuthenticatedUser = Depends(get_current_user_sse),
):
    """
    §SSE · Stream de eventos enfocado en un siniestro específico.
    """
    queue_id, queue = sse_manager.subscribe(
        user_id=user.usuario_id,
        role=user.rol,
        aseguradora_id=user.aseguradora_id,
    )

    async def event_generator():
        init_frame = sse_manager.format_sse_frame(
            event="connected",
            data={"message": f"Suscrito a eventos del siniestro {id}", "siniestro_id": id},
        )
        yield init_frame

        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=15.0)
                    yield message
                except asyncio.TimeoutError:
                    yield sse_manager.format_ping()
        except asyncio.CancelledError:
            pass
        finally:
            sse_manager.unsubscribe(queue_id)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Content-Encoding": "none",
        },
    )
