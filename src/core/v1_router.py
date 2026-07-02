"""
Superficie canónica `/api/v1` con prefijos por rol (sección 0 del spec).

Reúne los routers por rol que reutilizan los casos de uso existentes. Se monta
en `core/routers.py` bajo el prefijo `/v1`. Las rutas previas (no versionadas)
se mantienen temporalmente para no romper integraciones en tránsito.
"""
from fastapi import APIRouter

from src.modules.cliente.presentation.v1.cliente_v1_routes import router as cliente_v1_router
from src.modules.ajustador.presentation.ajustador_routes import router as ajustador_v1_router
from src.modules.taller.presentation.v1.taller_v1_routes import router as taller_v1_router
from src.modules.aseguradora.presentation.v1.aseguradora_v1_routes import router as aseguradora_v1_router
from src.modules.admin.presentation.v1.admin_v1_routes import router as admin_v1_router
from src.modules.auth.presentation.v1.auth_v1_routes import router as auth_v1_router
from src.modules.aseguradora.presentation.v1.aseguradora_crud_v1_routes import router as aseguradora_crud_v1_router

v1_router = APIRouter()
v1_router.include_router(cliente_v1_router, prefix="/cliente", tags=["v1 · Cliente"])
v1_router.include_router(ajustador_v1_router, prefix="/ajustador", tags=["v1 · Ajustador"])
v1_router.include_router(taller_v1_router, prefix="/taller", tags=["v1 · Taller"])
v1_router.include_router(aseguradora_v1_router, prefix="/aseguradora", tags=["v1 · Aseguradora"])
v1_router.include_router(admin_v1_router, prefix="/admin", tags=["v1 · Admin"])
v1_router.include_router(auth_v1_router, prefix="/auth", tags=["v1 · Auth"])
v1_router.include_router(aseguradora_crud_v1_router, prefix="/aseguradora/crud", tags=["v1 · Aseguradora CRUD"])
