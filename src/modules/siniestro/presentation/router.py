from fastapi import APIRouter
from src.modules.siniestro.presentation.siniestros.siniestro_routes import router as siniestros_router
from src.modules.siniestro.presentation.peritaje.peritaje_routes import router as peritaje_router

router = APIRouter()
router.include_router(siniestros_router)
router.include_router(peritaje_router)
