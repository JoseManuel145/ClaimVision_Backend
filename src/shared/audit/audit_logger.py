"""
Auditoría transversal. La regla global del spec exige que *toda mutación*
escriba en `logs_auditoria`. Este servicio reutiliza el repositorio de auditoría
existente (módulo admin) y expone una API simple e independiente de HTTP.

Se usa desde la capa de presentación tras una mutación exitosa:

    @router.post(...)
    def endpoint(request: Request, user=Depends(...), audit=Depends(get_audit_logger)):
        resultado = usecase.execute(...)
        audit.record(
            usuario=user,
            evento_modulo="cliente.siniestros",
            accion="reportar_siniestro",
            request=request,
            metadata={"siniestro_id": resultado.id},
        )
        return resultado

La escritura nunca interrumpe el flujo principal: si la auditoría falla se
registra el error y la petición continúa.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from src.core.database import get_session
from src.core.logging import get_logger
from src.modules.admin.domain.models import AuditLog
from src.modules.admin.infra.db.repositories.audit_log_repository import AuditLogRepository
from src.modules.auth.domain.models import AuthenticatedUser

logger = get_logger("audit")


def client_ip(request: Optional[Request]) -> str:
    if request is None or request.client is None:
        return "unknown"
    return request.client.host or "unknown"


def user_agent(request: Optional[Request]) -> str:
    if request is None:
        return "unknown"
    return request.headers.get("user-agent", "unknown")


class AuditLogger:
    def __init__(self, session: Session):
        self._repo = AuditLogRepository(session)

    def record(
        self,
        *,
        evento_modulo: str,
        accion: str,
        usuario: Optional[AuthenticatedUser] = None,
        usuario_id: Optional[str] = None,
        aseguradora_id: Optional[str] = None,
        request: Optional[Request] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        try:
            log = AuditLog(
                id=str(uuid.uuid4()),
                usuario_id=usuario_id or (usuario.usuario_id if usuario else None),
                aseguradora_id=aseguradora_id
                or (usuario.aseguradora_id if usuario else None),
                evento_modulo=evento_modulo,
                accion_realizada=accion,
                direccion_ip=client_ip(request),
                user_agent=user_agent(request),
                metadata_context=metadata,
                created_at=datetime.now(timezone.utc),
            )
            self._repo.append(log)
        except Exception as exc:  # la auditoría jamás rompe el flujo principal
            logger.error(f"No se pudo escribir en logs_auditoria: {exc}", exc_info=True)


def get_audit_logger(session: Session = Depends(get_session)) -> AuditLogger:
    return AuditLogger(session)
