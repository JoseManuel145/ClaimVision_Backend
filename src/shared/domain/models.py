from enum import Enum
from dataclasses import dataclass

class Rol(Enum):
    SUPER_ADMINISTRADOR = "Administrador_Global"
    ASEGURADORA = "Operador_Aseguradora"
    AJUSTADOR = "Ajustador"
    TALLER = "Operador_Taller"
    CLIENTE = "Cliente"
    TESTER = "Tester_Global"

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

class AccionAudit(Enum):
    ACTUALIZAR_AJUSTADOR = "actualizar_ajustador"
    ACTUALIZAR_CLIENTE = "actualizar_cliente"
    ACTUALIZAR_CONSENTIMIENTOS = "actualizar_consentimientos"
    ACTUALIZAR_COTIZACION = "actualizar_cotizacion"
    ACTUALIZAR_DISPONIBILIDAD = "actualizar_disponibilidad"
    ACTUALIZAR_SUSCRIPCION = "actualizar_suscripcion"
    ACTUALIZAR_TALLER = "actualizar_taller"
    ACTUALIZAR_USUARIO = "actualizar_usuario"
    ACTUALIZAR_VEHICULO = "actualizar_vehiculo"
    AGREGAR_DANO = "agregar_dano"
    APROBAR_COTIZACION = "aprobar_cotizacion"
    ASIGNAR_AJUSTADOR = "asignar_ajustador"
    AUTORIZAR_ENTREGA = "autorizar_entrega"
    BLOQUEO_ARCO = "bloqueo_arco"
    CONCLUIR_TRABAJO = "concluir_trabajo"
    CONFIRMAR_DATOS = "confirmar_datos"
    CREAR_AJUSTADOR = "crear_ajustador"
    CREAR_CLIENTE = "crear_cliente"
    CREAR_COTIZACION = "crear_cotizacion"
    CREAR_DESDE_POLIZA = "crear_desde_poliza"
    CREAR_OPERADOR = "crear_operador"
    CREAR_OPERADOR_TALLER = "crear_operador_taller"
    CREAR_TALLER = "crear_taller"
    CREAR_USUARIO = "crear_usuario"
    CREAR_VEHICULO = "crear_vehiculo"
    CREAR_VEHICULO_DESDE_POLIZA = "crear_vehiculo_desde_poliza"
    DESBLOQUEO_ARCO = "desbloqueo_arco"
    DESINCORPORAR_ASEGURADORA = "desincorporar_aseguradora"
    EDITAR_PERITAJE = "editar_peritaje"
    EDITAR_SINIESTRO = "editar_siniestro"
    ELIMINAR_AJUSTADOR = "eliminar_ajustador"
    ELIMINAR_TALLER = "eliminar_taller"
    ELIMINAR_USUARIO = "eliminar_usuario"
    ELIMINAR_VEHICULO = "eliminar_vehiculo"
    ENVIAR_TALLER = "enviar_taller"
    LISTO_ENTREGA = "listo_entrega"
    PURGA_ASEGURADORA = "purga_aseguradora"
    REACTIVAR_ASEGURADORA = "reactivar_aseguradora"
    RECHAZAR_COTIZACION = "rechazar_cotizacion"
    REGISTRAR_AJUSTADOR = "registrar_ajustador"
    REGISTRAR_PERITAJE = "registrar_peritaje"
    REGISTRAR_ASEGURADORA = "registrar_aseguradora"
    REPORTAR_SINIESTRO = "reportar_siniestro"
    SUBIR_IMAGEN = "subir_imagen"
    VERIFICAR_ASEGURADORA = "verificar_aseguradora"