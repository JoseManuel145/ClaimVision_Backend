from fastapi import APIRouter
from src.modules.taller.presentation.expedientes.expedientes_routes import router as expedientes_router
from src.modules.taller.presentation.presupuestos.presupuestos_routes import router as presupuestos_router

router = APIRouter()
router.include_router(expedientes_router)
router.include_router(presupuestos_router)
