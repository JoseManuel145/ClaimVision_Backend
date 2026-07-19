"""Router canónico `/api/v1` con prefijos por rol."""
from fastapi import APIRouter

from src.modules.cliente.presentation.cliente_v1_routes import router as cliente_v1_router
from src.modules.ajustador.presentation.ajustador_v1_routes import router as ajustador_v1_router
from src.modules.taller.presentation.taller_v1_routes import router as taller_v1_router
from src.modules.aseguradora.presentation.siniestros.siniestro_routes import router as aseguradora_router
from src.modules.aseguradora.presentation.ajustadores.ajustador_routes import router as ajustador_crud_router
from src.modules.aseguradora.presentation.clientes.cliente_routes import router as cliente_crud_router
from src.modules.aseguradora.presentation.talleres.taller_routes import router as taller_crud_router
from src.modules.aseguradora.presentation.usuarios.usuario_routes import router as usuario_crud_router
from src.modules.aseguradora.presentation.vehiculos.vehiculo_routes import router as vehiculo_crud_router
from src.modules.aseguradora.presentation.perfil.perfil_routes import router as perfil_router
from src.modules.admin.presentation.admin_v1_routes import router as admin_v1_router
from src.modules.auth.presentation.auth_v1_routes import router as auth_v1_router
from src.modules.ia_bridge.presentation.ia_bridge_v1_routes import router as ia_bridge_router
from src.shared.presentation.sse_routes import router as sse_router

api_router = APIRouter()
api_router.include_router(cliente_v1_router, prefix="/v1/cliente", tags=["v1 · Cliente"])
api_router.include_router(ajustador_v1_router, prefix="/v1/ajustador", tags=["v1 · Ajustador"])
api_router.include_router(taller_v1_router, prefix="/v1/taller", tags=["v1 · Taller"])
api_router.include_router(aseguradora_router, prefix="/v1/aseguradora", tags=["v1 · Aseguradora"])
api_router.include_router(ajustador_crud_router, prefix="/v1/aseguradora/crud/ajustadores", tags=["v1 · Aseguradora CRUD"])
api_router.include_router(cliente_crud_router, prefix="/v1/aseguradora/crud/clientes", tags=["v1 · Aseguradora CRUD"])
api_router.include_router(taller_crud_router, prefix="/v1/aseguradora/crud/talleres", tags=["v1 · Aseguradora CRUD"])
api_router.include_router(usuario_crud_router, prefix="/v1/aseguradora/crud/usuarios", tags=["v1 · Aseguradora CRUD"])
api_router.include_router(vehiculo_crud_router, prefix="/v1/aseguradora/crud/vehiculos", tags=["v1 · Aseguradora CRUD"])
api_router.include_router(perfil_router, prefix="/v1/aseguradora/perfil", tags=["v1 · Aseguradora"])
api_router.include_router(admin_v1_router, prefix="/v1/admin", tags=["v1 · Admin"])
api_router.include_router(auth_v1_router, prefix="/v1/auth", tags=["v1 · Auth"])
api_router.include_router(ia_bridge_router, prefix="/v1/ia", tags=["v1 · IA Bridge"])
api_router.include_router(sse_router, prefix="/v1")

