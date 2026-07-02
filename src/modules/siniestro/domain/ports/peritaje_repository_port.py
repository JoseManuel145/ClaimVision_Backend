from typing import Optional
from src.modules.siniestro.domain.models.peritaje_model import PeritajeAjustadorModel

class PeritajeAjustadorRepositoryPort:
    def guardar_peritaje(self, peritaje: PeritajeAjustadorModel) -> PeritajeAjustadorModel:
        """Guarda o actualiza un peritaje y sus daños manuales."""
        pass
    
    def obtener_peritaje_por_siniestro(self, siniestro_id: str) -> Optional[PeritajeAjustadorModel]:
        """Obtiene el peritaje de un ajustador dado el ID del siniestro."""
        pass

    def obtener_por_id(self, peritaje_id: str) -> Optional[PeritajeAjustadorModel]:
        """Obtiene un peritaje por su ID."""
        pass

    def get_by_siniestro(self, siniestro_id: str) -> Optional[PeritajeAjustadorModel]:
        """Alias de `obtener_peritaje_por_siniestro` (usado por el módulo taller)."""
        pass
