from datetime import datetime
import uuid
from src.modules.siniestro.domain.models.siniestro_model import SiniestroModel
from src.modules.siniestro.domain.ports.siniestro_repository_port import SiniestroRepositoryPort
from src.modules.siniestro.presentation.siniestros.siniestro_dto import SiniestroInicializarDTO
from src.modules.siniestro.domain.ports.cliente_checker_port import ClienteCheckerPort
from src.shared.domain.models import EstatusSiniestro
from src.core.exceptions import BusinessRuleError

class InicializarSiniestro:
    def __init__(self, repo: SiniestroRepositoryPort, cliente_checker: ClienteCheckerPort):
        self.repo = repo
        self.cliente_checker = cliente_checker

    def execute(self, cliente_id: str, aseguradora_id: str, dto: SiniestroInicializarDTO) -> SiniestroModel:
        # 1. Validar que el cliente tenga onboarding (perfil de cliente)
        perfil_cliente_id = self.cliente_checker.get_perfil_cliente_id_by_usuario(cliente_id)
        if not perfil_cliente_id:
            raise BusinessRuleError("Debe completar su registro de póliza (Onboarding) antes de reportar un siniestro.")

        siniestro = SiniestroModel(
            id=str(uuid.uuid4()),
            aseguradora_id=aseguradora_id,
            cliente_id=perfil_cliente_id,
            ajustador_id=None,
            taller_id=None,
            estatus=EstatusSiniestro.REPORTADO_PRELIMINAR.value,
            vehiculo_marca=dto.vehiculo_marca,
            vehiculo_modelo=dto.vehiculo_modelo,
            vehiculo_anio=dto.vehiculo_anio,
            vehiculo_placas=dto.vehiculo_placas,
            vehiculo_vin=dto.vehiculo_vin,
            latitud_siniestro=dto.latitud_siniestro,
            longitud_siniestro=dto.longitud_siniestro,
            narracion_texto=dto.narracion_texto,
            narracion_audio_url=dto.narracion_audio_url,
            indicaciones_dano_interno=dto.indicaciones_dano_interno,
            fecha_siniestro=dto.fecha_siniestro or datetime.utcnow(),
            version=1,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            deleted_at=None
        )
        return self.repo.save(siniestro)
