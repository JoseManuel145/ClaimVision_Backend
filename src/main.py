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

@app.on_event("startup")
def create_missing_tables():
    Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Root"])
def root():
    return {"Status": "OK"}

if __name__ == "__main__":
    print("Documentacion Interactiva: http://127.0.0.1:8000/docs")
    print("Documentacion Descriptiva: http://127.0.0.1:8000/redoc")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

