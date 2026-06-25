from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SiniestroTecnicoDTO(BaseModel):
    id: str
    estatus: str
    vehiculo_marca: str
    vehiculo_modelo: str
    vehiculo_anio: int
    vehiculo_vin: Optional[str]
    narracion_texto: Optional[str]
    indicaciones_dano_interno: bool
    fecha_siniestro: datetime
    
class DanoAjustadoDTO(BaseModel):
    zona_vehiculo: str
    tipo: str
    severidad: str
    
class PeritajeAjustadorTecnicoDTO(BaseModel):
    observaciones_campo: Optional[str]
    danos_ajustados: List[DanoAjustadoDTO]
    
class CotizacionTallerDTO(BaseModel):
    monto_mano_obra: float
    monto_refacciones: float
    monto_total: float
    desglose_pdf_url: str
    estatus: str
    observaciones_tecnicas: Optional[str]

class ExpedienteTecnicoResponseDTO(BaseModel):
    siniestro: SiniestroTecnicoDTO
    peritaje_ajustador: Optional[PeritajeAjustadorTecnicoDTO]
    cotizacion: Optional[CotizacionTallerDTO]

class GuardarPresupuestoRequestDTO(BaseModel):
    monto_mano_obra: float
    monto_refacciones: float
    observaciones_tecnicas: Optional[str] = None
    
class MessageResponseDTO(BaseModel):
    message: str
