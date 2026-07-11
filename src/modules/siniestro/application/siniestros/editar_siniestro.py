from datetime import datetime
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.presentation.siniestros.siniestro_dto import SiniestroUpdateDTO
from src.core.exceptions import NotFoundError, BusinessRuleError
from src.shared.domain.models import EstatusSiniestro

class EditarSiniestro:
    def __init__(self, repo: SiniestroRepositoryPort):
        self.repo = repo

    def execute(self, siniestro_id: str, usuario_id: str, rol: str, dto: SiniestroUpdateDTO) -> SiniestroModel:
        siniestro = self.repo.get_by_id(siniestro_id)
        if not siniestro:
            raise NotFoundError("Siniestro no encontrado")

        # Reglas de negocio básicas para la edición
        # Un cliente solo puede editar si es suyo
        if rol == "Cliente" and siniestro.cliente_id != usuario_id:
            raise BusinessRuleError("No tiene permiso para editar este siniestro")
            
        # Un ajustador solo puede editar si está asignado a este siniestro
        if rol == "Ajustador" and siniestro.ajustador_id != usuario_id:
            raise BusinessRuleError("No tiene permiso para editar este siniestro. No le ha sido asignado.")
            
        # Actualización condicional
        if dto.vehiculo_id is not None:
            siniestro.vehiculo_id = dto.vehiculo_id
        if dto.vehiculo_marca is not None:
            siniestro.vehiculo_marca = dto.vehiculo_marca
        if dto.vehiculo_modelo is not None:
            siniestro.vehiculo_modelo = dto.vehiculo_modelo
        if dto.vehiculo_anio is not None:
            siniestro.vehiculo_anio = dto.vehiculo_anio
        if dto.vehiculo_placas is not None:
            siniestro.vehiculo_placas = dto.vehiculo_placas
        if dto.vehiculo_vin is not None:
            siniestro.vehiculo_vin = dto.vehiculo_vin
        if dto.latitud_siniestro is not None:
            siniestro.latitud_siniestro = dto.latitud_siniestro
        if dto.longitud_siniestro is not None:
            siniestro.longitud_siniestro = dto.longitud_siniestro
        if dto.narracion_texto is not None:
            siniestro.narracion_texto = dto.narracion_texto
        if dto.narracion_audio_url is not None:
            siniestro.narracion_audio_url = dto.narracion_audio_url
        if dto.indicaciones_dano_interno is not None:
            siniestro.indicaciones_dano_interno = dto.indicaciones_dano_interno

        siniestro.updated_at = datetime.utcnow()
        
        return self.repo.update(siniestro)
