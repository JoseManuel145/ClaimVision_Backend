from fastapi import HTTPException
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.domain.ports.peritaje_repository_port import PeritajeAjustadorRepositoryPort
from src.modules.taller.domain.models.cotizacion_model import CotizacionTallerModel
from src.modules.taller.domain.ports.cotizacion_repository_port import CotizacionRepositoryPort
from src.modules.taller.domain.ports.perfil_taller_port import PerfilTallerRepositoryPort
from src.modules.taller.domain.ports.pdf_generator_port import PdfGeneratorPort
from src.modules.taller.domain.ports.pdf_storage_port import PdfStoragePort
from src.shared.domain.models import EstatusCotizacion
from datetime import datetime, timezone
import uuid

class GuardarPresupuestoUseCase:
    def __init__(
        self,
        siniestro_repo: SiniestroRepositoryPort,
        peritaje_repo: PeritajeAjustadorRepositoryPort,
        cotizacion_repo: CotizacionRepositoryPort,
        perfil_taller_repo: PerfilTallerRepositoryPort,
        pdf_generator: PdfGeneratorPort,
        pdf_storage: PdfStoragePort
    ):
        self.siniestro_repo = siniestro_repo
        self.peritaje_repo = peritaje_repo
        self.cotizacion_repo = cotizacion_repo
        self.perfil_taller_repo = perfil_taller_repo
        self.pdf_generator = pdf_generator
        self.pdf_storage = pdf_storage

    async def execute(
        self, 
        siniestro_id: str, 
        usuario_id: str, 
        monto_mano_obra: float, 
        monto_refacciones: float,
        observaciones_tecnicas: str | None = None
    ) -> CotizacionTallerModel:
        taller_id = self.perfil_taller_repo.get_taller_id_by_usuario(usuario_id)
        if not taller_id:
            raise HTTPException(status_code=403, detail="El usuario no tiene un perfil de taller asignado.")
            
        siniestro = self.siniestro_repo.get_by_id(siniestro_id)
        if not siniestro:
            raise HTTPException(status_code=404, detail="Siniestro no encontrado.")
            
        if siniestro.taller_id != taller_id:
            raise HTTPException(status_code=403, detail="Este expediente no está asignado a tu taller.")
            
        peritaje = self.peritaje_repo.get_by_siniestro(siniestro_id)
        if not peritaje:
            raise HTTPException(status_code=400, detail="No se puede cotizar sin un peritaje previo del ajustador.")
            
        monto_total = monto_mano_obra + monto_refacciones
        
        # Build PDF context
        context = {
            "Siniestro ID": siniestro_id,
            "Vehiculo": f"{siniestro.vehiculo_marca} {siniestro.vehiculo_modelo} {siniestro.vehiculo_anio}",
            "Placas": siniestro.vehiculo_placas,
            "Monto Mano de Obra": f"${monto_mano_obra:,.2f}",
            "Monto Refacciones": f"${monto_refacciones:,.2f}",
            "Monto Total Cotizado": f"${monto_total:,.2f}",
            "Daños Ajustados": [f"{d.zona_vehiculo} - {d.tipo} ({d.severidad})" for d in peritaje.danos_ajustados],
            "Observaciones": observaciones_tecnicas or "Ninguna"
        }
        
        # Generate PDF
        pdf_bytes = self.pdf_generator.generate_pdf(context)
        
        # Upload PDF
        filename = f"cotizacion_{siniestro_id}.pdf"
        pdf_url = await self.pdf_storage.upload_pdf(pdf_bytes, filename)
        
        cotizacion_existente = self.cotizacion_repo.get_by_siniestro(siniestro_id)
        
        if cotizacion_existente:
            # Update
            cotizacion_existente.monto_mano_obra = monto_mano_obra
            cotizacion_existente.monto_refacciones = monto_refacciones
            cotizacion_existente.monto_total = monto_total
            cotizacion_existente.desglose_pdf_url = pdf_url
            cotizacion_existente.observaciones_tecnicas = observaciones_tecnicas
            cotizacion_existente.estatus = EstatusCotizacion.PENDIENTE_APROBACION.value
            cotizacion_existente.updated_at = datetime.now(timezone.utc)
            return self.cotizacion_repo.save(cotizacion_existente)
        else:
            # Create
            nueva_cotizacion = CotizacionTallerModel(
                id=str(uuid.uuid4()),
                siniestro_id=siniestro_id,
                taller_id=taller_id,
                monto_mano_obra=monto_mano_obra,
                monto_refacciones=monto_refacciones,
                monto_total=monto_total,
                desglose_pdf_url=pdf_url,
                estatus=EstatusCotizacion.PENDIENTE_APROBACION.value,
                observaciones_tecnicas=observaciones_tecnicas,
                version=1,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            return self.cotizacion_repo.save(nueva_cotizacion)
