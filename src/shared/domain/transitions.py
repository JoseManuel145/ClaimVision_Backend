"""
Máquina de estados del ciclo de vida de un siniestro (`estatus_siniestro`).

Define las transiciones válidas y un validador central reutilizable por todos
los casos de uso que cambian el estatus, para garantizar que el flujo del spec
se respete (Reportado → Asignado_A_Ajustador → Peritaje_Validado →
Asignado_A_Taller → Trabajo_Concluido → Listo_Para_Entrega → Entregado).
"""
from src.shared.domain.models import EstatusSiniestro
from src.core.exceptions import BusinessRuleError

# Mapa: estatus_actual -> {estatus_destino válidos}
SINIESTRO_TRANSICIONES: dict[str, set[str]] = {
    EstatusSiniestro.REPORTADO_PRELIMINAR.value: {
        EstatusSiniestro.ASIGNADO_A_AJUSTADOR.value,
    },
    EstatusSiniestro.ASIGNADO_A_AJUSTADOR.value: {
        EstatusSiniestro.PERITAJE_VALIDADO.value,
    },
    EstatusSiniestro.PERITAJE_VALIDADO.value: {
        EstatusSiniestro.ASIGNADO_A_TALLER.value,
    },
    EstatusSiniestro.ASIGNADO_A_TALLER.value: {
        EstatusSiniestro.TRABAJO_CONCLUIDO.value,
    },
    EstatusSiniestro.TRABAJO_CONCLUIDO.value: {
        EstatusSiniestro.LISTO_PARA_ENTREGA.value,
    },
    EstatusSiniestro.LISTO_PARA_ENTREGA.value: {
        EstatusSiniestro.ENTREGADO.value,
    },
    EstatusSiniestro.ENTREGADO.value: set(),  # estado terminal
}


# Orden lineal del ciclo de vida (para construir el timeline de seguimiento).
SINIESTRO_ORDEN: list[str] = [
    EstatusSiniestro.REPORTADO_PRELIMINAR.value,
    EstatusSiniestro.ASIGNADO_A_AJUSTADOR.value,
    EstatusSiniestro.PERITAJE_VALIDADO.value,
    EstatusSiniestro.ASIGNADO_A_TALLER.value,
    EstatusSiniestro.TRABAJO_CONCLUIDO.value,
    EstatusSiniestro.LISTO_PARA_ENTREGA.value,
    EstatusSiniestro.ENTREGADO.value,
]


def construir_timeline(estatus_actual: str) -> list[dict]:
    """
    Devuelve la línea de tiempo del siniestro como lista ordenada de etapas con
    bandera `alcanzado` según el estatus actual. Útil para la vista de
    seguimiento del cliente (no hay tabla de historial en el esquema).
    """
    try:
        idx_actual = SINIESTRO_ORDEN.index(estatus_actual)
    except ValueError:
        idx_actual = -1
    return [
        {"estatus": estatus, "alcanzado": i <= idx_actual, "actual": i == idx_actual}
        for i, estatus in enumerate(SINIESTRO_ORDEN)
    ]


def transicion_valida(actual: str, destino: str) -> bool:
    """Indica si pasar de `actual` a `destino` es una transición permitida."""
    return destino in SINIESTRO_TRANSICIONES.get(actual, set())


def validar_transicion(actual: str, destino: str) -> None:
    """
    Valida una transición de estatus. Lanza `BusinessRuleError` (409) si no es
    válida. Es idempotente sólo en el sentido de que rechaza moverse al mismo
    estado salvo que el mapa lo permita explícitamente.
    """
    if actual == destino:
        raise BusinessRuleError(
            f"El siniestro ya se encuentra en estatus '{actual}'."
        )
    if not transicion_valida(actual, destino):
        raise BusinessRuleError(
            f"Transición de estatus inválida: '{actual}' → '{destino}'."
        )
