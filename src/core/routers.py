from fastapi import APIRouter
from src.modules.auth.presentation.routes import router as auth_router
from src.modules.cliente.presentation.routes import router as cliente_router
from src.modules.admin.presentation.routes import router as admin_router
from src.modules.aseguradora.presentation.router import router as aseguradora_router
from src.modules.siniestro.presentation.router import router as siniestro_router
from src.modules.taller.presentation.router import router as taller_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
api_router.include_router(aseguradora_router, prefix="/aseguradora", tags=["Aseguradora"])
api_router.include_router(siniestro_router, prefix="/siniestros", tags=["Siniestros"])
api_router.include_router(taller_router, prefix="/taller", tags=["Taller"])
