import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.routers import api_router
from src.core.logging import setup_logging

setup_logging()
app = FastAPI(
    title="ClaimVision-API",
    description="API del proyecto ClaimVision, en constante actualizacion y mejoria",
    docs_url="/docs",
    redoc_url="/redoc",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bienvenido a ClaimVision API"}

if __name__ == "__main__":
    print("Documentacion Interactiva: http://127.0.0.1:8000/docs")
    print("Documentacion Descriptiva: http://127.0.0.1:8000/redoc")
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)

