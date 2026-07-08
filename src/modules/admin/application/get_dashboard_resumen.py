from sqlalchemy.orm import Session
from sqlalchemy import select, func, text
from src.modules.siniestro.infra.db.tables.siniestro_table import SiniestroTable
from src.modules.auth.infra.db.tables.user_table import UserTable
from src.modules.admin.infra.db.tables.aseguradora_table import AseguradoraTable
from src.modules.aseguradora.infra.db.tables.taller_table import TallerTable
from src.shared.domain.models import EstatusSiniestro, EstadoUsuario, EstatusComercialAseguradora

class GetDashboardResumen:
    def __init__(self, db: Session):
        self.db = db

    def execute(self) -> dict:
        total_siniestros = self.db.execute(
            select(func.count()).select_from(SiniestroTable).where(SiniestroTable.deleted_at.is_(None))
        ).scalar() or 0

        status_rows = self.db.execute(
            select(SiniestroTable.estatus, func.count().label("count"))
            .where(SiniestroTable.deleted_at.is_(None))
            .group_by(SiniestroTable.estatus)
            .order_by(SiniestroTable.estatus)
        ).all()

        siniestros_por_estatus = [
            {"estatus": row.estatus.value if hasattr(row.estatus, 'value') else row.estatus, "count": row.count}
            for row in status_rows
        ]

        mes_rows = self.db.execute(
            text("""
                SELECT to_char(created_at, 'YYYY-MM') as mes, COUNT(*) as count
                FROM siniestros
                WHERE deleted_at IS NULL
                GROUP BY mes
                ORDER BY mes
            """)
        ).all()

        siniestros_por_mes = [{"mes": row.mes, "count": row.count} for row in mes_rows]

        usuarios_activos = self.db.execute(
            select(func.count()).select_from(UserTable).where(
                UserTable.fecha_eliminacion.is_(None),
                UserTable.estatus_arco != EstadoUsuario.INACTIVO.value,
            )
        ).scalar() or 0

        total_aseguradoras = self.db.execute(
            select(func.count()).select_from(AseguradoraTable)
        ).scalar() or 0

        aseguradoras_activas = self.db.execute(
            select(func.count()).select_from(AseguradoraTable).where(
                AseguradoraTable.deleted_at.is_(None),
                AseguradoraTable.estatus_comercial != EstatusComercialAseguradora.CANCELADO.value,
            )
        ).scalar() or 0

        total_talleres = self.db.execute(
            select(func.count()).select_from(TallerTable).where(TallerTable.deleted_at.is_(None))
        ).scalar() or 0

        talleres_pendientes = self.db.execute(
            select(func.count()).select_from(TallerTable).where(TallerTable.deleted_at.is_(None))
        ).scalar() or 0

        return {
            "total_siniestros": total_siniestros,
            "siniestros_por_estatus": siniestros_por_estatus,
            "siniestros_por_mes": siniestros_por_mes,
            "usuarios_activos": usuarios_activos,
            "total_aseguradoras": total_aseguradoras,
            "aseguradoras_activas": aseguradoras_activas,
            "total_talleres": total_talleres,
            "talleres_pendientes": talleres_pendientes,
        }
