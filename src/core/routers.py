from fastapi import APIRouter
from src.core.v1_router import v1_router

api_router = APIRouter()
# Superficie canónica versionada (sección 0 del spec): /api/v1/<rol>/...
api_router.include_router(v1_router, prefix="/v1")
