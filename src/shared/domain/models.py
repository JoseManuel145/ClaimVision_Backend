from enum import Enum
from dataclasses import dataclass

class Rol(str, Enum):
    SUPER_ADMINISTRADOR = "Administrador_Global"
    ASEGURADORA = "Operador_Aseguradora"
    AJUSTADOR = "Ajustador"
    TALLER = "Operador_Taller"
    CLIENTE = "Cliente"

class EstadoUsuario(str, Enum):
    ACTIVO = "Activo"
    BLOQUEADO_ARCO = "Bloqueado_ARCO"
    BLOQUEADO_TEMPORAL = "Bloqueado_Temporal"
    INACTIVO = "Inactivo"
