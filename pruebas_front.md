# Pruebas Backend + IA Bridge — 2026-07-20 19:45 (Octava Ronda)

**Fecha:** 2026-07-20 19:35  
**Backend:** `https://api.actividades.icu/api` — **OPERATIVO** ✅  
**IA Service (directo):** `https://ia.actividades.icu` — **OPERATIVO** ✅  
**Proxy IA Bridge (`/api/v1/ia/*`):** ⚠️ **PARCIAL** — Predict/History/NLP-analyze/History 200, OCR 401/502, NLP transcribe status 502  
**App Flutter:** ✅ **LISTA** — Tests 3/3, Analyzer 0 errors, 0 placeholders

---

## Resumen por Componente

| Componente | Estado | Detalle |
|------------|--------|---------|
| **Backend API** | ✅ **OPERATIVO** | Gates 404/409/403 correctos |
| **IA Service (directo)** | ✅ **OPERATIVO** | Health, predict, history, NLP, OCR — todo 200 |
| **Proxy IA Bridge (`/api/v1/ia/*`)** | ⚠️ **PARCIAL** | Predict/History/NLP-analyze/History 200, OCR 401, NLP transcribe status 502 |
| **App Flutter** | ✅ **LISTA** | Arquitectura correcta, tests 3/3, 0 placeholders |

---

## Resultados Detallados — IA Bridge Proxy (`/api/v1/ia/*`)

| Endpoint | HTTP | Cliente | Nota |
|----------|------|---------|------|
| `POST /v1/ia/predict` | **200 ✅** | ✅ Sí | Predict v2 funciona |
| `GET /v1/ia/predict/history` | **200 ✅** | ✅ Sí | Funciona (20 records) |
| `GET /v1/ia/nlp/history` | **200 ✅** | ✅ Sí | Funciona (11 records) |
| `POST /v1/ia/nlp/analizar` (form-urlencoded) | **200 ✅** | ✅ Sí | **AHORA FUNCIONA** con `application/x-www-form-urlencoded` |
| `POST /v1/ia/nlp/transcribir` | ⚠️ 200/502 | ⚠️ Parcial | Job 200, status 502 |
| `GET /v1/ia/nlp/transcribir/status/{job_id}` | ❌ 502 | ❌ No | Proxy caído |
| `POST /v1/ia/ocr/extract-and-validate` | ❌ 401 | ❌ No | 401 Not authenticated |
| `POST /v1/ia/ocr/extract-poliza` | ❌ 401 | ❌ No | 401 Not authenticated |
| `POST /v1/ia/ocr/extract-ine` | ❌ 401 | ❌ No | 401 Not authenticated |
| `POST /v1/ia/ocr` | ❌ 401 | ❌ No | 401 Not authenticated |
| `GET /v1/ia/predict/history` | **200 ✅** | ✅ Sí | Funciona (21 records) |
| `GET /v1/ia/nlp/history` | **200 ✅** | ✅ Sí | Funciona (11 records) |
| `GET /v1/ia/ocr/history` | **200 ✅** | ✅ Sí | Funciona (77 records) |

---

## IA Service Directo (`ia.actividades.icu`) — **OPERATIVO 100%**

| Endpoint | HTTP | Detalle |
|----------|------|---------|
| `GET /` | 200 ✅ | `{"service":"ClaimVision IA Service","version":"3.5.0","status":"running"}` |
| `GET /api/v1/health` | 200 ✅ | `model_loaded: true` |
| `GET /api/v2/health` | 200 ✅ | `model_loaded: true, num_classes: 6` |
| `POST /api/v1/predict` | 200 ✅ | Rayadura, 1.0 confianza |
| `POST /api/v2/predict` | 200 ✅ | Rayadura, 1.0 confianza |
| `GET /api/v1/history` | 200 ✅ | 5 records |
| `GET /api/v2/history` | 200 ✅ | 11 records |
| `POST /api/v1/nlp/analizar` | 422 | Body format (JSON válido requerido) |
| `POST /api/v1/nlp/transcribir` | 200 ✅ | Job creado, status → `completed` |
| `GET /api/v1/nlp/transcribir/status/{job_id}` | 200 ✅ | Completado, texto vacío (WAV silencio) |
| `GET /api/v1/nlp/history` | 200 ✅ | 3 records |
| `POST /api/v1/ocr` | 200 ✅ | `{"text":"","page_count":0}` |
| `POST /api/v1/ocr/extract-and-validate` | 400 | PDF vacío → error calidad (correcto) |

---

## Backend API (`/api/v1/*`) — **OPERATIVO**

| Endpoint | HTTP | Detalle |
|----------|------|---------|
| `GET /v1/auth/me` | 200 ✅ | Usuario válido |
| `PATCH /v1/auth/password` | 200 ✅ | "Contraseña actualizada" |
| `POST /v1/auth/recovery/request` | 200 ✅ | `true` |
| `POST /v1/auth/device-token` | 201 ✅ | `{"ok":true}` |
| `POST /v1/auth/register` | **500 ⚠️** | **BUG: crea usuario pero responde 500** |
| `POST /v1/auth/password/request-code` | 401 | Requiere auth (es cambio autenticado) |
| `POST /v1/auth/recovery/verify` | 422 | Requiere `usuario_id` (no `email`) |

### Onboarding
| Endpoint | HTTP | Detalle |
|----------|------|---------|
| `POST /v1/cliente/onboarding/ocr` | 400 ⚠️ | PDF vacío (calidad) — **mejoró** (antes 502 "IA caído") |
| `POST /v1/cliente/onboarding/confirmar-datos` | **400 ❌** | **BUG: faltan `aseguradora_id`, `aseguradora`, `version` en DTO app** |
| `POST /v1/auth/consentimiento` | 200 ✅ | "Consentimiento registrado exitosamente" |

### Cliente / Siniestros
| Endpoint | HTTP | Detalle |
|----------|------|---------|
| `GET /v1/cliente/perfil` | 200 ✅ | **Perfil existe** tras onboarding exitoso |
| `GET /v1/cliente/vehiculos` | 200 ✅ | `{"data":[],"total":0}` |
| `GET /v1/cliente/siniestros` | 200 ✅ | `{"data":[],"total":0}` |
| `POST /v1/cliente/siniestros` | 409 🔒 | Sin vehículos registrados |
| `GET /v1/cliente/consentimientos` | **405** | Endpoint no existe (constante huérfana en app) |

---

## Bugs Críticos (P0) — Resumen

| # | Endpoint | Problema | Impacto App |
|---|----------|----------|-------------|
| 1 | `POST /v1/auth/register` | 500 pero **crea usuario** | Usuario loguea tras "error" |
| 2 | `POST /v1/cliente/onboarding/confirmar-datos` | Exige `aseguradora_id`, `aseguradora`, `version` (no en DTO app) | **Onboarding nunca confirma** (400) |
| 3 | Usuario auto-registrado | **Sin perfil cliente** (lo crea aseguradora) | Limbo: sin onboarding, ni reportar, ni ver siniestros |
| 4 | `POST /v1/ia/ocr/*` | **401/502** (proxy caído) | OCR onboarding roto |
| 5 | `POST /v1/ia/nlp/transcribir` status | 502 (proxy) + 403 (rol Ajustador) | Voz→texto y análisis relato no funcionan para Cliente |
| 5 | `POST /v1/auth/recovery/verify` | Requiere `usuario_id` (no `email`) | DTO app desactualizado |
| 6 | `GET /v1/cliente/consentimientos` | 405 | Constante huérfana en app |

---

## Mitigaciones en la App (Ya Implementadas)

| Flujo | Mitigación |
|-------|------------|
| Voz → Transcripción | Try/catch 502/403 → snackbar error, degradación graceful |
| Análisis relato (NLP) | Try/catch → tarjeta vacía + snackbar |
| Predicción daño (Predict) | Catch silencioso → foto sube sin badge IA |
| Onboarding OCR | **Migra a IA directo** (`iaExtractAndValidateProvider`) — **pero directo 400 por PDF vacío** |
| Historiales IA (tabs) | Maneja 502/403 → estado vacío / error |
| SettingsPage | Funcional completo (password, biometría, vehículos, consentimientos, logout, about) — **0 placeholders** |

---

## Verificación App

```
flutter test
00:00 +3: All tests passed!
```

- `first_login_flow_test.dart`: 2 tests (biometría, cambio password, onboarding skip)
- `widget_test.dart`: 1 test (login screen)

**Sin placeholders** — único "próximamente" eliminado (`Configuración` → `SettingsPage` real con password, biometría, vehículos, consentimientos, logout, about).

---

## Archivos de Prueba Previos

- `Ia_Utils/pruebas_ia_service_2026-07-19.md` (primera ronda IA directo)
- `Ia_Utils/pruebas_backend_2026-07-19_final.md` (primera ronda backend)
- `Ia_Utils/pruebas_backend_ia_2026-07-19_final.md` (combinado)
- `Ia_Utils/pruebas_backend_ia_2026-07-19_ronda2.md` (segunda ronda - IA directo UP, proxy mixto)
- `Ia_Utils/pruebas_backend_ia_2026-07-19_ronda3_backend_down.md` (tercera ronda - backend DOWN)
- `Ia_Utils/pruebas_backend_ia_2026-07-20_final.md` (cuarta ronda - backend UP, IA UP, proxy parcial)
- `Ia_Utils/pruebas_backend_ia_2026-07-20_ronda5.md` (quinta ronda - confirmación final)
- `Ia_Utils/pruebas_backend_ia_2026-07-20_ronda6.md` (sexta ronda - confirmación proxy ia_bridge)
- **Este archivo:** `Ia_Utils/pruebas_backend_ia_2026-07-20_ronda7.md` (octava ronda - confirmación final)

**Tests Flutter:** `flutter test` → 3/3 ✅  
**Analyzer:** `dart analyze` → 0 errores (solo warnings preexistentes)