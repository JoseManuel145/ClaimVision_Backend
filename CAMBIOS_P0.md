# Cambios P0 — ClaimVision Backend

> Resumen de todo lo modificado y agregado al implementar los endpoints P0
> (`/api/v1`) del flujo central. **43 tests pasando.** Nada se commiteó todavía.

---

## TL;DR — respuesta a las 3 preguntas

1. **¿Qué endpoints existentes modifiqué o renombré?**
   **Ninguna ruta existente se renombró ni se cambió de path.** Todas las rutas
   viejas siguen funcionando en su URL original. Lo nuevo vive bajo `/api/v1/...`
   (superficie aditiva). Solo modifiqué *código interno* (DTOs/usecases/repos) de
   forma compatible hacia atrás — detalle abajo.

2. **¿Toqué los 4 endpoints originales (login + asignar-ajustador / enviar-taller / autorizar-entrega)?**
   **No se rompió ninguno.**
   - `login`: **intacto**, sin cambios.
   - `asignar-ajustador`, `enviar-taller`, `autorizar-entrega`: sus **rutas y
     usecases originales siguen igual**. Lo que hice fue **exponer una copia** de
     esas acciones bajo `/api/v1/aseguradora/...` reutilizando los mismos usecases
     (asignar/enviar) y, para *autorizar-entrega*, una **versión nueva** corregida
     (`AutorizarEntregaV1`) — sin tocar la original. No hay nada que restaurar.

3. **¿Aditivo o reescribí código que ya funcionaba?**
   **99% aditivo.** Creé módulos/archivos nuevos. En archivos existentes solo
   **agregué** métodos/campos. La única línea de *comportamiento* que cambié fue en
   `InicializarSiniestro` (ahora respeta `fecha_siniestro`/`indicaciones_dano_interno`
   del DTO en vez de forzar valores fijos) — y es compatible: si el cliente no manda
   esos campos, se comporta igual que antes.

---

## Archivos EXISTENTES modificados (11) — todos compatibles hacia atrás

| Archivo | Qué cambié | Tipo | Por qué |
|---|---|---|---|
| `src/core/routers.py` | Agregué `include_router(v1_router, prefix="/v1")` | Aditivo | Montar la superficie `/api/v1`. No quita rutas viejas. |
| `src/core/security.py` | Agregué `require_roles(*roles)` | Aditivo | Dependencia RBAC reutilizable. `get_current_user` quedó intacto. |
| `src/modules/siniestro/presentation/siniestros/siniestro_dto.py` | Agregué 3 campos opcionales a `SiniestroInicializarDTO` (`narracion_audio_url`, `indicaciones_dano_interno=False`, `fecha_siniestro=None`) | Aditivo | El reporte del cliente (§4) necesita esos campos. Opcionales → no rompe llamadas previas. |
| `src/modules/siniestro/application/siniestros/inicializar_siniestro.py` | Usa esos campos del DTO en vez de `None`/`False`/`utcnow()` fijos | **Cambio de comportamiento (compatible)** | Antes ignoraba fecha/indicaciones. Si no se mandan, usa los mismos defaults de antes. |
| `src/modules/siniestro/domain/ports/siniestro_repository_port.py` | Agregué `list_by_cliente`; amplié firma de `list_by_aseguradora` con filtros opcionales | Aditivo | "Mis siniestros" (§4) y filtros de bandeja (§3). Params nuevos son opcionales. |
| `src/modules/siniestro/infra/db/repositories/siniestro_repository.py` | Implementé `list_by_cliente`; agregué filtros `ajustador_id/taller_id/q` a `list_by_aseguradora` | Aditivo | Igual que arriba. La firma vieja sigue válida (defaults). |
| `src/modules/siniestro/domain/ports/peritaje_repository_port.py` | Agregué `obtener_por_id` y alias `get_by_siniestro` | Aditivo | `obtener_por_id` para editar peritaje por id (§5); `get_by_siniestro` porque el módulo taller ya lo invocaba pero **no existía** (bug latente). |
| `src/modules/siniestro/infra/db/repositories/peritaje_repository.py` | Implementé esos 2 métodos | Aditivo + **fix** | El alias arregla `get_expediente`/`guardar_presupuesto` que llamaban un método inexistente. |
| `src/modules/taller/domain/ports/cotizacion_repository_port.py` | Agregué `get_by_id` | Aditivo | Editar/aprobar/rechazar cotización por su id (§3/§6). |
| `src/modules/taller/infra/db/repositories/cotizacion_repository.py` | Implementé `get_by_id` | Aditivo | Igual que arriba. |
| `requirements.txt` | Agregué `pytest` y `pytest-asyncio` | Aditivo | No había framework de tests instalado. |

> **Resumen del diff:** `11 files changed, 120 insertions(+), 11 deletions(-)`.
> Las 11 "deletions" son las 6 líneas reemplazadas en `inicializar_siniestro.py`
> (3 viejas→3 nuevas) y reformateos de firma; **no se borró ninguna función ni ruta.**

---

## Archivos NUEVOS creados (no tocan nada existente)

**Fundación transversal**
- `src/shared/domain/transitions.py` — validador de transiciones de `estatus_siniestro` + timeline.
- `src/shared/presentation/pagination.py` — envelope `{data,total,page,page_size}` del spec.
- `src/shared/audit/audit_logger.py` — auditoría reutilizable (reusa el repo de admin).
- `src/core/v1_router.py` — agregador de routers `/api/v1` por rol.

**§4 Cliente**
- `src/modules/cliente/presentation/v1/` (routes, dependencies, schemas)
- `src/modules/cliente/application/get_perfil_cliente.py`
- `src/modules/siniestro/application/siniestros/{list_siniestros_cliente,get_siniestro_cliente,registrar_imagen}.py`

**§5 Ajustador**
- `src/modules/ajustador/application/{asignaciones,peritaje,perfil}.py`
- `src/modules/ajustador/presentation/{ajustador_routes,ajustador_dependencies,ajustador_schemas}.py`

**§6 Taller**
- `src/modules/taller/application/cotizaciones_v1.py`
- `src/modules/taller/application/expedientes/marcar_listo_entrega.py`
- `src/modules/taller/presentation/v1/` (routes, dependencies, schemas)

**§3 Aseguradora**
- `src/modules/aseguradora/application/siniestros/{bandeja,autorizar_entrega_v1}.py`
- `src/modules/aseguradora/application/cotizaciones/aprobar_rechazar.py`
- `src/modules/aseguradora/presentation/v1/` (routes, dependencies, schemas)

**Tests / config**
- `tests/` (conftest, fakes y 4 archivos de pruebas, 43 tests)
- `pytest.ini`

---

## Conflicto importante que resolví (no es ruptura, es corrección)

El usecase legacy `AutorizarEntrega` hace `Trabajo_Concluido → Listo_Para_Entrega`,
pero el **spec §3** dice `autorizar-entrega → Entregado` (y `listo-entrega` lo hace
el taller en §6). **No toqué el usecase legacy.** Para `/api/v1` creé
`AutorizarEntregaV1` con la transición correcta (`Listo_Para_Entrega → Entregado`).

Flujo final correcto:
`… → Trabajo_Concluido →` (taller `listo-entrega`) `→ Listo_Para_Entrega →`
(aseguradora `autorizar-entrega`) `→ Entregado`.

---

## Cómo verificar que nada se rompió

```bash
./venv/Scripts/python.exe -m pytest tests/ -q   # 43 passed
```
Las rutas viejas (`/api/auth/login`, `/api/aseguradora/...`, `/api/siniestros/...`,
`/api/taller/...`) **siguen registradas y sin cambios de contrato**. Lo nuevo es
puramente aditivo bajo `/api/v1/...`.
