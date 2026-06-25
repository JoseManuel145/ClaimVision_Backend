from fastapi import Depends
from src.core.database import get_session
from sqlalchemy.orm import Session
from src.core.supabase import get_supabase_client
from src.modules.siniestro.infra.db.repositories.siniestro_repository import SiniestroRepository
from src.modules.siniestro.infra.db.repositories.peritaje_repository import PeritajeAjustadorRepository
from src.modules.taller.infra.db.repositories.cotizacion_repository import CotizacionRepository
from src.modules.taller.infra.db.repositories.perfil_taller_repository import PerfilTallerRepository
from src.modules.taller.infra.pdf.pdf_generator import ReportLabPdfGenerator
from src.modules.taller.infra.pdf.supabase_storage_repository import SupabasePdfStorage
from src.modules.taller.application.expedientes.list_expedientes import ListExpedientesTallerUseCase
from src.modules.taller.application.expedientes.get_expediente import GetExpedienteTallerUseCase
from src.modules.taller.application.expedientes.concluir_expediente import ConcluirExpedienteUseCase
from src.modules.taller.application.presupuestos.guardar_presupuesto import GuardarPresupuestoUseCase

def get_siniestro_repo(db: Session = Depends(get_session)):
    return SiniestroRepository(db)

def get_peritaje_repo(db: Session = Depends(get_session)):
    return PeritajeAjustadorRepository(db)

def get_cotizacion_repo(db: Session = Depends(get_session)):
    return CotizacionRepository(db)

def get_perfil_taller_repo(db: Session = Depends(get_session)):
    return PerfilTallerRepository(db)

def get_pdf_generator():
    return ReportLabPdfGenerator()

def get_pdf_storage():
    client = get_supabase_client()
    return SupabasePdfStorage(client)

def list_expedientes_taller_service(
    siniestro_repo=Depends(get_siniestro_repo),
    perfil_taller_repo=Depends(get_perfil_taller_repo)
):
    return ListExpedientesTallerUseCase(siniestro_repo, perfil_taller_repo)

def get_expediente_taller_service(
    siniestro_repo=Depends(get_siniestro_repo),
    peritaje_repo=Depends(get_peritaje_repo),
    cotizacion_repo=Depends(get_cotizacion_repo),
    perfil_taller_repo=Depends(get_perfil_taller_repo)
):
    return GetExpedienteTallerUseCase(siniestro_repo, peritaje_repo, cotizacion_repo, perfil_taller_repo)

def guardar_presupuesto_service(
    siniestro_repo=Depends(get_siniestro_repo),
    peritaje_repo=Depends(get_peritaje_repo),
    cotizacion_repo=Depends(get_cotizacion_repo),
    perfil_taller_repo=Depends(get_perfil_taller_repo),
    pdf_generator=Depends(get_pdf_generator),
    pdf_storage=Depends(get_pdf_storage)
):
    return GuardarPresupuestoUseCase(
        siniestro_repo, peritaje_repo, cotizacion_repo, perfil_taller_repo, pdf_generator, pdf_storage
    )

def concluir_expediente_service(
    siniestro_repo=Depends(get_siniestro_repo),
    cotizacion_repo=Depends(get_cotizacion_repo),
    perfil_taller_repo=Depends(get_perfil_taller_repo)
):
    return ConcluirExpedienteUseCase(siniestro_repo, cotizacion_repo, perfil_taller_repo)
