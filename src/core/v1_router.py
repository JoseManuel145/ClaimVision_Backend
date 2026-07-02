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

v1_router = APIRouter()
v1_router.include_router(cliente_v1_router)
v1_router.include_router(ajustador_v1_router)
v1_router.include_router(taller_v1_router)
v1_router.include_router(aseguradora_v1_router)
