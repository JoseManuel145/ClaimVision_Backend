import asyncio
import json
import pytest
from src.shared.infra.events.sse_manager import SSEManager, sse_manager
from src.core.security import get_current_user_sse
from src.modules.auth.domain.models import AuthenticatedUser
from src.core.exceptions import UnauthorizedError


def test_format_sse_frame():
    mgr = SSEManager()
    frame = mgr.format_sse_frame(event="siniestro_updated", data={"id": "123"}, event_id="evt_1")
    assert "id: evt_1" in frame
    assert "event: siniestro_updated" in frame
    assert 'data: {"id": "123"}' in frame


@pytest.mark.asyncio
async def test_sse_manager_subscribe_and_publish():
    mgr = SSEManager()
    queue_id, queue = mgr.subscribe(user_id="user_1", role="Cliente", aseguradora_id="aseg_1")
    
    assert queue_id.startswith("user_1_")
    
    # Publicar evento dirigido a aseguradora 1
    await mgr.publish_event(
        event="siniestro_created",
        data={"siniestro_id": "sin_99"},
        target_aseguradora_id="aseg_1",
    )
    
    frame = await asyncio.wait_for(queue.get(), timeout=2.0)
    assert "event: siniestro_created" in frame
    assert "sin_99" in frame
    
    mgr.unsubscribe(queue_id)


@pytest.mark.asyncio
async def test_sse_manager_isolation_by_user():
    mgr = SSEManager()
    qid1, q1 = mgr.subscribe(user_id="user_1", role="Cliente")
    qid2, q2 = mgr.subscribe(user_id="user_2", role="Cliente")

    # Evento específico para user_1
    await mgr.publish_event(
        event="perfil_updated",
        data={"user_id": "user_1"},
        target_user_id="user_1",
    )

    frame1 = await asyncio.wait_for(q1.get(), timeout=2.0)
    assert "user_1" in frame1

    assert q2.empty()

    mgr.unsubscribe(qid1)
    mgr.unsubscribe(qid2)


from unittest.mock import MagicMock

def test_get_current_user_sse_with_token_param():
    token_service = MagicMock()
    token_service.verify.return_value = MagicMock(
        usuario_id="user_123",
        email="test@claimvision.com",
        rol="Cliente",
        aseguradora_id="aseg_1",
    )

    user = get_current_user_sse(
        token="valid_jwt_token",
        auth_header=None,
        token_service=token_service,
    )

    assert user.usuario_id == "user_123"
    assert user.rol == "Cliente"
    assert user.aseguradora_id == "aseg_1"



def test_get_current_user_sse_without_token():
    with pytest.raises(UnauthorizedError):
        get_current_user_sse(token=None, auth_header=None, token_service=None)


@pytest.mark.asyncio
async def test_sse_manager_broadcast_same_aseguradora():
    """Verifica que dos usuarios distintos de la misma aseguradora reciban el evento."""
    mgr = SSEManager()
    qid1, q1 = mgr.subscribe(user_id="user_A", role="Operador_Aseguradora", aseguradora_id="aseg_100")
    qid2, q2 = mgr.subscribe(user_id="user_B", role="Operador_Aseguradora", aseguradora_id="aseg_100")
    qid3, q3 = mgr.subscribe(user_id="user_C", role="Operador_Aseguradora", aseguradora_id="aseg_999")

    # Publicar evento para la aseguradora 100
    await mgr.publish_event(
        event="cliente_created",
        data={"cliente_id": "c_1"},
        target_aseguradora_id="aseg_100",
    )

    frame1 = await asyncio.wait_for(q1.get(), timeout=2.0)
    frame2 = await asyncio.wait_for(q2.get(), timeout=2.0)

    assert "c_1" in frame1
    assert "c_1" in frame2
    assert q3.empty()

    mgr.unsubscribe(qid1)
    mgr.unsubscribe(qid2)
    mgr.unsubscribe(qid3)

