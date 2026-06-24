from fastapi import APIRouter
from .ajustadores.ajustador_routes import router as ajustadores_router
from .clientes.cliente_routes import router as clientes_router
from .talleres.taller_routes import router as talleres_router
from .siniestros.siniestro_routes import router as siniestros_router
from .usuarios.usuario_routes import router as usuarios_router

router = APIRouter(prefix="/v1/aseguradora", tags=["Aseguradora"])

router.include_router(ajustadores_router, prefix="/ajustadores")
router.include_router(clientes_router, prefix="/clientes")
router.include_router(talleres_router, prefix="/talleres")
router.include_router(siniestros_router, prefix="/siniestros")
router.include_router(usuarios_router, prefix="/usuarios")
