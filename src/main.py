import uvicorn
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from src.core.logging import setup_logging
from src.core.middlewares import register_middlewares
from src.core.exceptions import register_exception_handlers
from src.core.routers import api_router
from src.core.database import Base, engine
from src.core.rate_limit import limiter
from src.shared.infra.messaging.fcm_client import init_firebase

setup_logging()

app = FastAPI(
    title="ClaimVision-API",
    description="API del proyecto ClaimVision, en constante actualizacion y mejoria",
    docs_url="/docs",
    redoc_url="/redoc",
    version="1.12.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar middlewares transversales (CORS, Logging)
register_middlewares(app)

# Configurar manejadores de excepciones (Formateo de errores)
register_exception_handlers(app)

# Registrar todas las rutas de los módulos
app.include_router(api_router, prefix="/api")

from src.shared.infra.events.sse_manager import sse_manager
from src.core.config import settings

@app.on_event("startup")
async def startup_event():
    # Importar todas las tablas para registrarlas en Base.metadata
    from src.modules.admin.infra.db.tables.aseguradora_table import AseguradoraTable
    from src.modules.admin.infra.db.tables.audit_log_table import AuditLogTable
    from src.modules.aseguradora.infra.db.tables.ajustador_table import AjustadorTable
    from src.modules.aseguradora.infra.db.tables.convenio_table import ConvenioAseguradoraTallerTable
    from src.modules.aseguradora.infra.db.tables.perfil_cliente_table import PerfilClienteTable
    from src.modules.aseguradora.infra.db.tables.taller_table import TallerTable
    from src.modules.aseguradora.infra.db.tables.vehiculo_table import VehiculoTable
    from src.modules.auth.infra.db.tables.recovery_code import RecoveryCodeTable
    from src.modules.auth.infra.db.tables.user_table import UserTable
    from src.modules.cliente.infra.db.tables.cliente_documento_table import ClienteDocumentoTable
    from src.modules.cliente.infra.db.tables.cliente_profile_table import ClienteProfileTable
    from src.modules.siniestro.infra.db.tables.imagen_siniestro_table import ImagenSiniestroTable
    from src.modules.siniestro.infra.db.tables.peritaje_table import PeritajeAjustadorTable, DanosAjustadosManualTable
    from src.modules.siniestro.infra.db.tables.siniestro_table import SiniestroTable
    from src.modules.taller.infra.db.tables.cotizacion_table import CotizacionTallerTable
    from src.modules.taller.infra.db.tables.perfil_taller_table import PerfilTallerUsuariosTable
    from src.shared.infra.device_token.device_token_table import DeviceTokenTable

    Base.metadata.create_all(bind=engine)
    init_firebase()
    await sse_manager.init_redis(settings.REDIS_URL)

@app.on_event("shutdown")
async def shutdown_event():
    await sse_manager.close_redis()

@app.get("/", tags=["Root"])
def root():
    return {"Status": "OK"}

if __name__ == "__main__":
    print("Documentacion Interactiva: http://127.0.0.1:8000/docs")
    print("Documentacion Descriptiva: http://127.0.0.1:8000/redoc")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

