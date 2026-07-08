import uuid
from datetime import datetime, timezone
from src.modules.admin.domain.ports import AdminUserRepositoryPort, AuditLogRepositoryPort
from src.modules.admin.domain.models import AuditLog
from src.core.exceptions import NotFoundError, BusinessRuleError
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.modules.siniestro.infra.db.tables.siniestro_table import SiniestroTable
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.modules.aseguradora.infra.db.tables.ajustador_table import AjustadorTable
from src.modules.aseguradora.infra.db.tables.perfil_cliente_table import PerfilClienteTable as ClienteTable
from src.shared.domain.models import EstatusSiniestro


class DeleteUsuario:
    def __init__(self, user_repo: AdminUserRepositoryPort, audit_repo: AuditLogRepositoryPort, db: Session):
        self.user_repo = user_repo
        self.audit_repo = audit_repo
        self.db = db

    def execute(self, admin_id: str, usuario_id: str) -> dict:
        user = self.user_repo.get_by_id(usuario_id)
        if not user:
            raise NotFoundError("Usuario no encontrado.")

        profile_ids = self._get_profile_ids(usuario_id)
        active_siniestros = self._count_active_siniestros(profile_ids)
        if active_siniestros > 0:
            raise BusinessRuleError(
                f"El usuario tiene {active_siniestros} siniestro(s) activo(s). "
                "No se puede eliminar hasta que todos estén en estado 'Entregado'."
            )

        self.user_repo.soft_delete(usuario_id)

        self.audit_repo.append(AuditLog(
            id=str(uuid.uuid4()),
            usuario_id=admin_id,
            aseguradora_id=user.get("aseguradora_id"),
            accion_realizada="ELIMINAR_USUARIO",
            evento_modulo="USUARIOS",
            metadata_context={"usuario_id": usuario_id, "email_anonimizado": True},
            direccion_ip="[IP_ADDRESS]",
            user_agent=admin_id,
            created_at=datetime.now(),
        ))

        return self.user_repo.get_by_id(usuario_id)

    def _get_profile_ids(self, usuario_id: str) -> list:
        ids = []
        cliente = self.db.execute(
            select(ClienteTable.id).where(ClienteTable.usuario_id == usuario_id)
        ).scalar_one_or_none()
        if cliente:
            ids.append(("cliente_id", str(cliente)))

        ajustador = self.db.execute(
            select(AjustadorTable.id).where(AjustadorTable.usuario_id == usuario_id)
        ).scalar_one_or_none()
        if ajustador:
            ids.append(("ajustador_id", str(ajustador)))

        return ids

    def _count_active_siniestros(self, profile_ids: list) -> int:
        if not profile_ids:
            return 0
        final_status = EstatusSiniestro.ENTREGADO.value
        or_conditions = []
        for col, val in profile_ids:
            or_conditions.append(getattr(SiniestroTable, col) == val)
        from sqlalchemy import or_
        stmt = select(func.count()).select_from(SiniestroTable).where(
            or_(*or_conditions),
            SiniestroTable.deleted_at.is_(None),
            SiniestroTable.estatus != final_status,
        )
        return self.db.execute(stmt).scalar() or 0
