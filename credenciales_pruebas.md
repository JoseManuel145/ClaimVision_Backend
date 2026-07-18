# Credenciales de Prueba - ClaimVision

## Admin Global

| Campo | Valor |
|-------|-------|
| Email | `admin@claimvision.com` |
| Password | `SuperAdmin123!` |
| Rol | Administrador_Global |

---

## Aseguradora: Aseguradora Pruebas CI

- **ID:** `3821111f-9eea-4911-acc1-81b1c117bf13`
- **Plan:** Enterprise
- **RFC:** PCI861205XXX
- **Dominio:** pruebas-ci.com
- **Estatus:** Suspendido

### Gestor / Operador de la Aseguradora

| Campo | Valor |
|-------|-------|
| Email | `gestor@pruebas-ci.com` |
| Password | `GestorPru123!` |
| Rol | Operador_Aseguradora |

### Ajustadores

| # | Nombre | Email | Password | Licencia | Cédula |
|---|--------|-------|----------|----------|--------|
| 1 | Ajustador Uno | `ajustador1@pruebas-ci.com` | `AjusPru123!` | LIC-001 | CED-001 |
| 2 | Ajustador Dos | `ajustador2@pruebas-ci.com` | `AjusPru123!` | LIC-002 | CED-002 |

### Taller: Taller Pruebas CI

- **ID:** `7df598fe-6419-411d-8317-e9cf3e886819`
- **RFC:** TPC861205XXX
- **Dirección:** Av. Prueba 123, Col. Centro, CDMX
- **Teléfono:** +525533333333

#### Operador del Taller

| Campo | Valor |
|-------|-------|
| Email | `operador.taller@pruebas-ci.com` |
| Password | `OperPru123!` |
| Rol | Operador_Taller |

---

## Notas

- La aseguradora está en estado **Suspendido**. Para activarla, usar el endpoint:
  `POST /api/v1/admin/aseguradoras/{id}/verificar`
- Las contraseñas son temporales y deben cambiarse en el primer inicio de sesión.
