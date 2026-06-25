from enum import Enum
from dataclasses import dataclass

class Rol(Enum):
    SUPER_ADMINISTRADOR = "Administrador_Global"
    ASEGURADORA = "Operador_Aseguradora"
    AJUSTADOR = "Ajustador"
    TALLER = "Operador_Taller"
    CLIENTE = "Cliente"

class EstadoUsuario(Enum):
    ACTIVO = "Activo"
    BLOQUEADO_ARCO = "Bloqueado_ARCO"
    BLOQUEADO_TEMPORAL = "Bloqueado_Temporal"
    INACTIVO = "Inactivo"

class EstatusSiniestro(Enum):
    REPORTADO_PRELIMINAR = "Reportado_Preliminar"
    ASIGNADO_A_AJUSTADOR = "Asignado_A_Ajustador"
    PERITAJE_VALIDADO = "Peritaje_Validado"
    ASIGNADO_A_TALLER = "Asignado_A_Taller"
    TRABAJO_CONCLUIDO = "Trabajo_Concluido"
    LISTO_PARA_ENTREGA = "Listo_Para_Entrega"
    ENTREGADO = "Entregado"

class SeveridadDano(Enum):
    BAJO = "Bajo"
    MEDIO = "Medio"
    ALTO = "Alto"

class EstatusComercialAseguradora(Enum):
    ACTIVO = "Activo"
    SUSPENDIDO = "Suspendido"
    CANCELADO = "Cancelado"

class TipoDano(Enum):
    ABOLLADURA = "Abolladura"
    RAYADURA = "Rayadura"
    FRACTURA = "Fractura"
    ROTURA_CRISTAL = "Rotura_Cristal"
    DEFORMACION = "Deformacion"

class EstatusCotizacion(Enum):
    PENDIENTE_APROBACION = "Pendiente_Aprobacion"
    APROBADA = "Aprobada"
    RECHAZADA = "Rechazada"

class PlanSuscripcion(Enum):
    BASIC = "Basic"
    PRO = "Pro"
    ENTERPRISE = "Enterprise"

LIMITES_PLANES = {
    PlanSuscripcion.BASIC.value: 100,
    PlanSuscripcion.PRO.value: 500,
    PlanSuscripcion.ENTERPRISE.value: -1 # -1 indica ilimitado
}