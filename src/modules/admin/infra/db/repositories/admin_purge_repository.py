from typing import Dict
from sqlalchemy import text, select, delete as sa_delete, update as sa_update, func
from sqlalchemy.orm import Session

from src.modules.siniestro.infra.db.tables.siniestro_table import SiniestroTable
from src.modules.siniestro.infra.db.tables.imagen_siniestro_table import ImagenSiniestroTable
from src.modules.siniestro.infra.db.tables.peritaje_table import PeritajeAjustadorTable, DanosAjustadosManualTable
from src.modules.taller.infra.db.tables.cotizacion_table import CotizacionTallerTable
from src.modules.taller.infra.db.tables.perfil_taller_table import PerfilTallerUsuariosTable
from src.modules.aseguradora.infra.db.tables.perfil_cliente_table import PerfilClienteTable
from src.modules.aseguradora.infra.db.tables.ajustador_table import AjustadorTable
from src.modules.aseguradora.infra.db.tables.convenio_table import ConvenioAseguradoraTallerTable
from src.modules.aseguradora.infra.db.tables.taller_table import TallerTable
from src.modules.admin.infra.db.tables.aseguradora_table import AseguradoraTable
from src.modules.auth.infra.db.tables.user_table import UserTable


class AdminPurgeRepository:
    def __init__(self, session: Session):
        self.session = session

    def purge_aseguradora(self, aseguradora_id: str) -> Dict[str, int]:
        result: Dict[str, int] = {}
        try:
            siniestros_subq = select(SiniestroTable.id).where(
                SiniestroTable.aseguradora_id == aseguradora_id
            )
            usuarios_subq = select(UserTable.id).where(
                UserTable.aseguradora_id == aseguradora_id
            )

            # 1. danos_detectados_ia (sin clase ORM)
            result["danos_detectados_ia"] = self.session.execute(text("""
                DELETE FROM danos_detectados_ia
                WHERE peritaje_ia_id IN (
                    SELECT id FROM peritajes_ia
                    WHERE siniestro_id IN (
                        SELECT id FROM siniestros WHERE aseguradora_id = :aid
                    )
                )
            """), {"aid": aseguradora_id}).rowcount

            # 2. danos_ajustados_manual
            peritajes_subq = select(PeritajeAjustadorTable.id).where(
                PeritajeAjustadorTable.siniestro_id.in_(siniestros_subq)
            )
            result["danos_ajustados_manual"] = self.session.execute(
                sa_delete(DanosAjustadosManualTable).where(
                    DanosAjustadosManualTable.peritaje_ajustador_id.in_(peritajes_subq)
                )
            ).rowcount

            # 3. imagenes_siniestro
            result["imagenes_siniestro"] = self.session.execute(
                sa_delete(ImagenSiniestroTable).where(
                    ImagenSiniestroTable.siniestro_id.in_(siniestros_subq)
                )
            ).rowcount

            # 4. peritajes_ia (sin clase ORM)
            result["peritajes_ia"] = self.session.execute(text("""
                DELETE FROM peritajes_ia
                WHERE siniestro_id IN (
                    SELECT id FROM siniestros WHERE aseguradora_id = :aid
                )
            """), {"aid": aseguradora_id}).rowcount

            # 5. peritajes_ajustador
            result["peritajes_ajustador"] = self.session.execute(
                sa_delete(PeritajeAjustadorTable).where(
                    PeritajeAjustadorTable.siniestro_id.in_(siniestros_subq)
                )
            ).rowcount

            # 6. cotizaciones_taller
            result["cotizaciones_taller"] = self.session.execute(
                sa_delete(CotizacionTallerTable).where(
                    CotizacionTallerTable.siniestro_id.in_(siniestros_subq)
                )
            ).rowcount

            # 7. siniestros
            result["siniestros"] = self.session.execute(
                sa_delete(SiniestroTable).where(
                    SiniestroTable.aseguradora_id == aseguradora_id
                )
            ).rowcount

            # 8. perfiles_clientes
            result["perfiles_clientes"] = self.session.execute(
                sa_delete(PerfilClienteTable).where(
                    PerfilClienteTable.usuario_id.in_(usuarios_subq)
                )
            ).rowcount

            # 9. ajustadores
            result["ajustadores"] = self.session.execute(
                sa_delete(AjustadorTable).where(
                    AjustadorTable.usuario_id.in_(usuarios_subq)
                )
            ).rowcount

            # 10. perfiles_taller_usuarios
            result["perfiles_taller_usuarios"] = self.session.execute(
                sa_delete(PerfilTallerUsuariosTable).where(
                    PerfilTallerUsuariosTable.usuario_id.in_(usuarios_subq)
                )
            ).rowcount

            # 11. convenio_aseguradora_taller
            result["convenios"] = self.session.execute(
                sa_delete(ConvenioAseguradoraTallerTable).where(
                    ConvenioAseguradoraTallerTable.aseguradora_id == aseguradora_id
                )
            ).rowcount

            # 12. usuarios
            result["usuarios"] = self.session.execute(
                sa_delete(UserTable).where(
                    UserTable.aseguradora_id == aseguradora_id,
                    UserTable.aseguradora_id.isnot(None),
                )
            ).rowcount

            # 13. talleres huérfanos — usamos select() directamente en notin_()
            talleres_con_convenio_sq = (
                select(ConvenioAseguradoraTallerTable.taller_id)
                .where(ConvenioAseguradoraTallerTable.deleted_at.is_(None))
                .distinct()
            )
            result["talleres_eliminados"] = self.session.execute(
                sa_delete(TallerTable).where(
                    TallerTable.deleted_at.is_(None),
                    TallerTable.id.notin_(talleres_con_convenio_sq),
                )
            ).rowcount

            result["talleres_conservados"] = self.session.execute(
                select(func.count()).select_from(talleres_con_convenio_sq.subquery())
            ).scalar() or 0

            # 14. aseguradora — baja lógica
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)
            result["aseguradora_purgada"] = self.session.execute(
                sa_update(AseguradoraTable).where(
                    AseguradoraTable.id == aseguradora_id,
                    AseguradoraTable.deleted_at.is_(None),
                ).values(
                    deleted_at=now,
                    estatus_comercial="Cancelado",
                    updated_at=now,
                )
            ).rowcount

            self.session.commit()
            return result

        except Exception:
            self.session.rollback()
            raise
