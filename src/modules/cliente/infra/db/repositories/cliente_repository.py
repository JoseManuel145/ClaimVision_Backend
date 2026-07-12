from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from src.modules.cliente.domain.models import ClienteProfile
from src.modules.cliente.domain.ports import ClienteRepositoryPort
from src.modules.cliente.infra.db.tables.cliente_profile_table import ClienteProfileTable
from src.core.exceptions import NotFoundError

def _to_domain(obj: ClienteProfileTable) -> ClienteProfile:
    return ClienteProfile(
        id=str(obj.id),
        usuario_id=str(obj.usuario_id),
        numero_poliza=obj.numero_poliza,
        vigencia_poliza=obj.vigencia_poliza,
        curp_rfc_cifrado=obj.curp_rfc_cifrado,
        consentimiento_aviso_privacidad=obj.consentimiento_aviso_privacidad,
        consentimiento_biometria=obj.consentimiento_biometria,
        autoriza_transferencia_talleres=obj.autoriza_transferencia_talleres,
        fecha_consentimiento=obj.fecha_consentimiento,
        fecha_creacion=obj.created_at
    )

class ClienteRepository(ClienteRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def get_by_usuario_id(self, usuario_id: str) -> ClienteProfile | None:
        stmt = select(ClienteProfileTable).where(ClienteProfileTable.usuario_id == usuario_id)
        r = self.db.execute(stmt).scalar_one_or_none()
        if not r:
            return None
        return _to_domain(r)

    def save(self, profile: ClienteProfile) -> ClienteProfile:
        model = ClienteProfileTable(
            id=profile.id,
            usuario_id=profile.usuario_id,
            numero_poliza=profile.numero_poliza,
            vigencia_poliza=profile.vigencia_poliza,
            curp_rfc_cifrado=profile.curp_rfc_cifrado,
            consentimiento_aviso_privacidad=profile.consentimiento_aviso_privacidad,
            consentimiento_biometria=profile.consentimiento_biometria,
            autoriza_transferencia_talleres=profile.autoriza_transferencia_talleres,
            fecha_consentimiento=profile.fecha_consentimiento,
            fecha_creacion=profile.fecha_creacion or datetime.now(timezone.utc)
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return _to_domain(model)

    def update(self, profile: ClienteProfile) -> ClienteProfile:
        stmt = (
            update(ClienteProfileTable)
            .where(ClienteProfileTable.id == profile.id)
            .values(
                numero_poliza=profile.numero_poliza,
                vigencia_poliza=profile.vigencia_poliza,
                curp_rfc_cifrado=profile.curp_rfc_cifrado,
                consentimiento_aviso_privacidad=profile.consentimiento_aviso_privacidad,
                consentimiento_biometria=profile.consentimiento_biometria,
                autoriza_transferencia_talleres=profile.autoriza_transferencia_talleres,
                fecha_consentimiento=profile.fecha_consentimiento
            )
        )
        result = self.db.execute(stmt)
        if result.rowcount == 0:
            raise NotFoundError("Perfil de cliente no encontrado")
        self.db.commit()
        return self.get_by_usuario_id(profile.usuario_id)
