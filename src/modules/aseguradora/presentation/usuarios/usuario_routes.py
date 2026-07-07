from fastapi import APIRouter, Depends, Request

from src.core.security import require_roles
from src.modules.auth.domain.models import AuthenticatedUser
from src.shared.audit.audit_logger import AuditLogger, get_audit_logger

from src.modules.aseguradora.application.usuarios.bloqueo_arco import BloqueoArcoAseguradora
from src.modules.aseguradora.application.usuarios.desbloqueo_arco import DesbloqueoArcoAseguradora
from src.modules.aseguradora.presentation.usuarios import usuario_dependencies

router = APIRouter()

get_operador = require_roles("Operador_Aseguradora")
EVENTO = "aseguradora.crud"


@router.post("/{id}/bloqueo-arco")
def aplicar_bloqueo_arco(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: BloqueoArcoAseguradora = Depends(usuario_dependencies.bloqueo_arco_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    uc.execute(user.aseguradora_id, id)
    audit.record(
        evento_modulo=EVENTO, accion="bloqueo_arco",
        usuario=user, request=request,
        metadata={"usuario_id": id},
    )
    return {"message": "Bloqueo ARCO aplicado exitosamente"}


@router.post("/{id}/desbloqueo-arco")
def aplicar_desbloqueo_arco(
    id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_operador),
    uc: DesbloqueoArcoAseguradora = Depends(usuario_dependencies.desbloqueo_arco_service),
    audit: AuditLogger = Depends(get_audit_logger),
):
    uc.execute(user.aseguradora_id, id)
    audit.record(
        evento_modulo=EVENTO, accion="desbloqueo_arco",
        usuario=user, request=request,
        metadata={"usuario_id": id},
    )
    return {"message": "Desbloqueo ARCO aplicado exitosamente"}
