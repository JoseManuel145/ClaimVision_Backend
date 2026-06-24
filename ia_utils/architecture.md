# ARQUITECTURA QUE SE USARA EN EL PROYECTO

```
├── core                # Utilidades y configuración global (no lógica de negocio)
│   ├── config.py       # Carga y validación de variables de entorno
│   ├── database.py     # Inicialización de la base de datos y sesión
│   ├── exceptions.py   # Manejo centralizado de errores
│   ├── logging.py      # Configuración de logs
│   ├── routers.py      # Registro de rutas principales
│   ├── security.py     # Seguridad y utilidades criptográficas
│   └── supabase_config.py # Configuración de Supabase (almacenamiento)
├── modules             # Módulos funcionales, cada uno aislado
│   ├── module1         # Module 1
│   │   ├── application # Casos de uso
│   │   ├── domain      # Modelos y contratos del dominio
│   │   ├── infra       # Implementaciones técnicas (DB, JWT, Google, etc.)
│   │   └── presentation# Rutas y dependencias FastAPI
│   ├── module2         # Module 2
│   │   ├── app         # Casos de uso
│   │   ├── domain      # Modelos y contratos del dominio
│   │   ├── infra       # Implementaciones técnicas (DB, JWT, Google, etc.)
│   │   └── presentation# Rutas y DTOs
│   └──...
├── shared              # Utilidades compartidas entre módulos
└── main.py             # Punto de entrada de la aplicación FastAPI
```


> **Nota:** Cada subcarpeta dentro de `modules` representa un contexto de negocio independiente, siguiendo el principio de "bounded context".


#### `presentation/` (API)
Responsable únicamente de HTTP:
- Traduce requests → DTOs (Pydantic)
- Llama a casos de uso (application)
- Devuelve responses
> **Nunca contiene lógica de negocio.**

#### `application/` (Usecases)
Capa de aplicación:
- Implementa reglas de negocio a nivel de casos de uso
- Orquesta entidades del dominio y puertos
- No conoce FastAPI ni SQLAlchemy
> **Tip:** Aquí se valida la lógica de negocio y se aplican políticas.

#### `domain/`
Capa más importante:
- Modela el negocio (entidades, value objects)
- Define contratos (puertos/interfaces)
- No depende de ninguna otra capa
> **El dominio es intocable y estable.**

#### `infra/`
Detalles técnicos:
- Base de datos, ORM, servicios externos
- Implementa los contratos definidos en `domain/ports`
> **Nunca poner lógica de negocio aquí.**

#### `core/`
Soporte transversal:
- Configuración, logging, seguridad, inyección de dependencias
> **No contiene lógica de negocio, solo utilidades globales.**
## Puntos importantes / buenas prácticas

## Regla clave de dependencias

```
presentation → application → domain ← infra
```

El dominio **no depende de nada**.  
La infraestructura depende del dominio, nunca al revés.

## Puntos importantes / buenas prácticas

- **Seguridad de credenciales**
  - Nunca devolver el campo `password` (ni hashes) en responses.
  - El hash del password debe realizarse en el **usecase** (application), antes de persistir el usuario.
  - La capa `presentation` no debe conocer detalles de hashing.


- **Separación de modelos**
  - Mantener separados:
    - DTOs (Pydantic) → `presentation/schemas`
    - Entidades de dominio → `domain/models`
    - Modelos ORM → `infra/db/models`

- **Evitar dependencias cruzadas** para reducir acoplamiento.

## Ejemplo de los `__init__.py`:
```python
from .get_user_by_id import GetUserById
from .anonymize_user import AnonymizeUser
from .get_user_by_email import GetUserByEmail
from .delete_user import DeleteUser
from .get_all_users import GetAllUsers
from .update_user import UpdateUser
from .get_all_users import GetAllUsers
from .create_admin import CreateAdmin
from .get_admins import GetAllAdmins
from .register_device_token import RegisterDeviceToken
__all__ = [
    GetUserById,
    AnonymizeUser,
    GetUserByEmail,
    DeleteUser,
    GetAllUsers,
    UpdateUser,
    CreateAdmin,
    GetAllAdmins,
    RegisterDeviceToken
]
```

## Ejemplo de inyeccion de dependencias:
```python
from src.core.database import get_session
from fastapi import Depends

# repository
from src.modules.usuarios.infra.direccion_repository import DireccionRepository

# usecases
from src.modules.usuarios.application.direccion.get_all_direcciones import GetAllDirecciones
from src.modules.usuarios.application.direccion.get_direccion_by_id import GetDireccionById
from src.modules.usuarios.application.direccion.create_direccion import CreateDireccion
from src.modules.usuarios.application.direccion.update_direccion import UpdateDireccion
from src.modules.usuarios.application.direccion.delete_direccion import DeleteDireccion
from src.modules.usuarios.application.direccion.set_primary import SetPrimaryDireccion

def get_all_direcciones_service(session=Depends(get_session)):
    repo = DireccionRepository(session)
    return GetAllDirecciones(repo)

def get_direccion_service(session=Depends(get_session)):
    repo = DireccionRepository(session)
    return GetDireccionById(repo)

def create_direccion_service(session=Depends(get_session)):
    repo = DireccionRepository(session)
    return CreateDireccion(repo)

def update_direccion_service(session=Depends(get_session)):
    repo = DireccionRepository(session)
    return UpdateDireccion(repo)

def delete_direccion_service(session=Depends(get_session)):
    repo = DireccionRepository(session)
    return DeleteDireccion(repo)

def set_primary_service(session=Depends(get_session)):
    repo = DireccionRepository(session)
    return SetPrimaryDireccion(repo)
```

## Tips dentro de un modulo
Si un modulo comparte muchas features sera implementado asi


```
modules/
├── auth
│   ├── app # casos de uso
│   │   ├── __init__.py
│   │   └── ...
│   ├── domain
│   │   ├── models.py
│   │   └── ports.py
│   ├── infra
│   │   ├── db
│   │   │   ├── repositories
│   │   │   │   └── ...
│   │   │   └── tables
│   │   │       └── ...
│   │   ├── google
│   │   │   └── ...
│   │   ├── jwt
│   │   │   └── ...
│   │   ├── messaging
│   │   │   └── ...
│   │   └── security
│   │   │   └── ...
│   └── presentation
│       ├── dependencies.py
│       ├── routes.py
│       └── schemas.py
├── carrito
│   ├── app # casos de uso
│   │   ├── __init__.py
│   │   └── ...
│   ├── domain
│   │   ├── __init__.py
│   │   ├── carrito_model.py
│   │   └── carrito_port.py
│   ├── infra
│   │   ├── carrito_repository.py
│   │   └── carrito_table.py
│   └── presentation
│       ├── carrito_dependencies.py
│       ├── carrito_dto.py
│       └── carrito_routes.py
├── catalogo
│   ├── app # casos de uso
│   │   ├── categories
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── colors
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── images
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── products
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   ├── sections
│   │   │   ├── __init__.py
│   │   │   └── ...
│   │   └── sizes
│   │       ├── __init__.py
│   │   │   └── ...
│   ├── domain
│   │   ├── models # separados por feat
│   │   │   ├── __init__.py
│   │   │   ├── categoria_model.py
│   │   │   ├── color_model.py
│   │   │   ├── imagen_model.py
│   │   │   ├── producto_model.py
│   │   │   ├── seccion_model.py
│   │   │   └── talla_model.py
│   │   └── ports # separados por feat
│   │       ├── __init__.py
│   │       ├── categoria_port.py
│   │       ├── color_port.py
│   │       ├── imagen_port.py
│   │       ├── producto_port.py
│   │       ├── seccion_port.py
│   │       └── talla_port.py
│   ├── infra # cada feat tiene repositorio y su tabla
│   │   ├── category
│   │   │   └── ...
│   │   ├── colors
│   │   │   └── ...
│   │   ├── images
│   │   │   ├── db # indica que es la base de datos
│   │   │   │   └── ...
│   │   │   └── storage # indica que es de un bucket, como este caso
│   │   │       └── supabase_storage_repository.py # repositorio del bucket
│   │   ├── products
│   │   │   └── ...
│   │   ├── sections
│   │   │   └── ...
│   │   └── sizes
│   │       └── ...
│   └── presentation # cada feat tiene dtos, rutas y su dependencias (di)
│       ├── category
│       │   └── ...
│       ├── colors
│       │   └── ...
│       ├── images
│       │   └── ...
│       ├── products
│       │   └── ...
│       ├── section
│       │   └── ...
│       └── sizes
│           └── ...
```

### Muy importante seguir patrones de diseño como repository, ports, inversion de dependencias (inyeccion de dependencias/di), Strategy, Fouler, GoF, Factory, etc.
### Mantener el codigo modular y escalable para facilitar el mantenimiento y la adición de nuevas funcionalidades

---

## 3. NUEVAS DIRECTRICES AGREGADAS (V3.0)

### 3.1 Pautas de Asincronía (`async` / `await`)
Para maximizar el rendimiento de la API en tareas de alta latencia (Vision AI, OCR, llamadas de red, persistencia), adoptamos un flujo asíncrono en las capas superiores:
- **Presentation (`routes.py`)**: Todos los endpoints deben declararse con `async def` y ejecutar los casos de uso utilizando `await usecase.execute(...)`.
- **Application (`usecases`)**: El método `execute` de cada caso de uso debe ser `async def execute(...)`.
- Cuando un caso de uso recibe mas de dos variables, se debe crear un modelo para empaquetar esas variables y en el caso de uso se desempaquetan usando modelo.var1 modelo.var2...
- **Infraestructura**: Si se consumen servicios bloqueantes o síncronos (como el motor síncrono de SQLAlchemy/Postgres o APIs externas síncronas), se ejecutan directamente en la función asíncrona o se delegan a un pool de hilos mediante utilidades de FastAPI.

### 3.2 Patrón de Mapeo de Datos (Mappers)
Para mantener el desacoplamiento total prescrito en **Clean Architecture**, los modelos de base de datos (`UserTable`) **nunca** deben cruzar la frontera de la capa de infraestructura hacia la aplicación o presentación.
- Cada repositorio debe incluir una función pura de mapeo (ej: `_to_domain(obj_db: UserTable) -> AuthUser`).
- Esto nos permite cambiar de ORM (ej. de SQLAlchemy a Tortoise u ODM de MongoDB) sin cambiar una sola línea del caso de uso o del dominio.

```python
def _to_domain(r: UserTable) -> UserModel:
    return UserModel(
        usuario_id=r.usuario_id,
        nombre=r.nombre,
        email=r.email,
        telefono=r.telefono,
        rol=r.rol.value if r.rol else None,
        fecha_creacion=r.fecha_creacion,
        fecha_eliminacion=r.fecha_eliminacion,
    )
```

### 3.3 Gestión de Errores Limpios (Capa a Capa)
- **Dominio y Aplicación**: Lanzan excepciones nativas de Python (`ValueError`, `PermissionError`) o excepciones de negocio personalizadas (ej. `UserBlockedError`). **Nunca** deben levantar `HTTPException` directamente, ya que la capa de aplicación no debe saber nada sobre el protocolo HTTP.
- **Presentación (`routes.py` o manejadores globales)**: Atrapa estas excepciones de negocio y las traduce a las excepciones HTTP tipadas en `src/core/exceptions.py` (`NotFoundError`, `ForbiddenError`, `UnauthorizedError`) para responder al cliente de manera consistente.

### 3.4 Multi-Tenancy y Aislamiento (`aseguradora_id`)
ClaimVision es una plataforma SaaS multi-inquilino. Por lo tanto:
- Toda entidad ligada al negocio corporativo (usuarios, ajustadores, siniestros, cotizaciones) debe validar el `aseguradora_id`.
- Los **Super Administradores** tienen acceso global (`aseguradora_id = None`), pero los roles corporativos (`Operador_Aseguradora`, `Ajustador`) deben tener su consulta filtrada estrictamente por el `aseguradora_id` extraído del JWT en la capa de seguridad.
- Esta validación de permisos de tenencia debe realizarse en la capa de **Aplicación** (Caso de uso) tras recibir los datos validados del payload del token.
### Mantener el codigo modular y escalable para facilitar el mantenimiento y la adición de nuevas funcionalidades

