# REGISTRO DE ERRORES (KNOWLEDGE BASE)
Este documento es una memoria técnica evolutiva del proyecto. Cada vez que ocurra un error en tiempo de compilación, ejecución o diseño de infraestructura, la IA debe analizar la causa raíz, aplicar la solución y registrar el evento en este archivo siguiendo estrictamente el formato establecido para evitar regresiones de código.

---

## 1. Titulo del error (Ejemplo: Violación de Capas por Importación Circular en Módulos)
### Descripción del problema
El servidor de FastAPI falla al arrancar arrojando un `ImportError: cannot import name 'X' from partially initialized module 'Y'`. Esto ocurrió al intentar inyectar un servicio de la capa de infraestructura directamente dentro del constructor de un Caso de Uso en la capa de aplicación, rompiendo el principio de inversión de dependencias.

### Como se soluciono
Se aplicó el patrón de Inversión de Dependencias (SOLID D). Se definió una interfaz abstracta (`abc.ABC`) en `domain/ports.py`. El Caso de Uso ahora solo depende de esa abstracción pura. La implementación real del repositorio de infraestructura se inyecta dinámicamente en tiempo de ejecución a través del archivo `presentation/dependencies.py` utilizando el sistema `Depends` de FastAPI.

---

## 2. ModuleNotFoundError al ejecutar python src/main.py
### Descripción del problema
* **Contexto/Acción:** Intentando arrancar el servidor de FastAPI desde la terminal en el directorio raíz usando `python src/main.py` o directamente desde la carpeta `src/`.
* **Traceback/Mensaje de la Consola:**
```text
Traceback (most recent call last):
  File "/home/manu/Documentos/Clases/Proyecto Integrador/ClaimVision_Backend/src/main.py", line 4, in <module>
    from src.core.config import settings
ModuleNotFoundError: No module named 'src'
```

### Como se soluciono
* **Análisis de Causa Raíz:** Al arrancar el script `src/main.py` directamente, Python añade automáticamente el directorio contenedor (`src/`) al `sys.path` de búsqueda, pero no la raíz del proyecto. Esto hace que las importaciones absolutas del tipo `from src.xxx` no puedan resolverse.
* **Refactorización Aplicada:** 
  1. Se cambió el comando de ejecución para inicializar el módulo desde la raíz del proyecto utilizando el flag de módulo (`-m`): `PYTHONPATH=. python -m src.main`.
  2. Se ajustó en `src/main.py` la llamada a `uvicorn.run("src.main:app", ...)` en lugar de `uvicorn.run("main:app", ...)` para permitir la correcta recarga del servidor por parte del reloader process de Uvicorn.

---

## 3. ProgrammingError por Columnas No Existentes en la Base de Datos (google_id / is_authenticated)
### Descripción del problema
* **Contexto/Acción:** Ejecución de peticiones al endpoint `/register` o `/login` que interactúan con el repositorio de usuarios (`AuthRepository.get_by_email`).
* **Traceback/Mensaje de la Consola:**
```text
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedColumn) column usuarios.google_id does not exist
LINE 1: ...s_arco, usuarios.created_at, usuarios.deleted_at, usuarios.g...
                                                             ^
[SQL: SELECT usuarios.id, usuarios.aseguradora_id, usuarios.rol, usuarios.email, usuarios.password_hash, usuarios.nombre_completo_cifrado, usuarios.telefono_cifrado, usuarios.estatus_arco, usuarios.created_at, usuarios.deleted_at, usuarios.google_id, usuarios.is_authenticated 
FROM usuarios 
WHERE usuarios.email = %(email_1)s]
```

### Como se soluciono
* **Análisis de Causa Raíz:** El modelo de SQLAlchemy `UserTable` (`src/modules/auth/infra/db/tables/user_table.py`) definía las columnas `google_id` e `is_authenticated`, las cuales no existen en el esquema físico de la base de datos de producción (`usuarios` en `database.md`). Esto causaba que SQLAlchemy incluyera estas columnas inexistentes en la cláusula SELECT de cualquier consulta.
* **Refactorización Aplicada:**
  1. Se eliminaron las declaraciones de las columnas `google_id` e `is_authenticated` del modelo de SQLAlchemy `UserTable`.
  2. Se adaptó el mapeador `_to_domain` y el método `create` en `AuthRepository` para omitir y/o retornar valores predeterminados seguros (`None` y `False` respectivamente) sin realizar la consulta en base de datos.
  3. Se ajustaron los métodos complementarios del repositorio `get_by_google_id`, `verify_user` y `link_google` para evitar el acceso a dichas columnas.

---

## 4. ValueError: password cannot be longer than 72 bytes, truncate manually (Incompatibilidad passlib <-> bcrypt 4.1.0+)
### Descripción del problema
* **Contexto/Acción:** Al intentar hashear o verificar contraseñas durante el registro o login de un usuario.
* **Traceback/Mensaje de la Consola:**
```text
  File "/home/manu/Documentos/Clases/Proyecto Integrador/ClaimVision_Backend/venv/lib64/python3.14/site-packages/passlib/handlers/bcrypt.py", line 620, in _load_backend_mixin
    version = _bcrypt.__about__.__version__
              ^^^^^^^^^^^^^^^^
AttributeError: module 'bcrypt' has no attribute '__about__'
...
  File "/home/manu/Documentos/Clases/Proyecto Integrador/ClaimVision_Backend/venv/lib64/python3.14/site-packages/passlib/handlers/bcrypt.py", line 655, in _calc_checksum
    hash = _bcrypt.hashpw(secret, config)
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])
```

### Como se soluciono
* **Análisis de Causa Raíz:** Las versiones recientes del paquete `bcrypt` (4.1.0+ y 5.0.0+) cambiaron su comportamiento y eliminaron atributos internos de metadatos, además de arrojar un `ValueError` si la longitud del password es mayor a 72 bytes. La librería `passlib` (desactualizada desde 2020) no es compatible con estos cambios e intenta usar un dummy secreto largo al validar el backend de `bcrypt`, causando un fallo de inicialización crítico.
* **Refactorización Aplicada:**
  1. Se realizó un downgrade en el entorno virtual del paquete `bcrypt` a la versión estable `4.0.1` (`pip install bcrypt==4.0.1`), la cual es 100% compatible con `passlib`.
  2. Se fijó explícitamente `bcrypt==4.0.1` en `requirements.txt`.

---

## 5. ProgrammingError / InvalidTextRepresentation por Casing de Enums de PostgreSQL ('CLIENTE' vs 'Cliente')
### Descripción del problema
* **Contexto/Acción:** Al intentar registrar un usuario mediante la ruta `POST /register` insertando un registro en la tabla `usuarios` en Supabase.
* **Traceback/Mensaje de la Consola:**
```text
psycopg2.errors.InvalidTextRepresentation or ProgrammingError:
LINE 1: ...3-658e-44f7-9b4d-dc8a398dcf4c'::UUID, NULL::UUID, 'CLIENTE',...
                                                             ^
[SQL: INSERT INTO usuarios (id, aseguradora_id, rol, email, password_hash, nombre_completo_cifrado, telefono_cifrado, estatus_arco, created_at, deleted_at) VALUES (%(id)s::UUID, %(aseguradora_id)s::UUID, %(rol)s, %(email)s, %(password_hash)s, %(nombre_completo_cifrado)s, %(telefono_cifrado)s, %(estatus_arco)s, %(created_at)s, %(deleted_at)s)]
[parameters: {'id': 'c4c31f93-658e-44f7-9b4d-dc8a398dcf4c', 'rol': 'CLIENTE', 'estatus_arco': 'ACTIVO', ...}]
```

### Como se soluciono
* **Análisis de Causa Raíz:** La base de datos en Supabase tiene tipos ENUM de PostgreSQL definidos como `rol_usuario` ('Cliente', etc.) y `estatus_usuario` ('Activo', etc.) que son sensibles a mayúsculas y minúsculas. Al declarar las columnas en SQLAlchemy con `Enum(Rol)` y `Enum(EstadoUsuario)`, SQLAlchemy serializa por defecto el nombre del miembro de Python Enum (ej: `'CLIENTE'`, `'ACTIVO'`) en lugar del valor de texto (`'Cliente'`, `'Activo'`), lo cual causa una violación de tipo en PostgreSQL.
* **Refactorización Aplicada:**
  1. Se cambiaron los tipos de columna `rol` y `estatus_arco` en `UserTable` a `String`. Esto permite delegar la conversión/casting de enums directamente a PostgreSQL.
  2. Se ajustaron las funciones `create` y `_to_domain` de `AuthRepository` para mapear los valores de string del Enum directamente (`user.rol` -> `"Cliente"` y `user.estado` -> `"Activo"`), garantizando que PostgreSQL reciba los textos exactos requeridos por sus tipos de datos enum nativos.

---

## 6. TypeError: Object of type UUID is not JSON serializable al firmar JWT
### Descripción del problema
* **Contexto/Acción:** Ocurre durante la generación del JWT tras registrar o loguear a un usuario exitosamente en la ruta `POST /register`.
* **Traceback/Mensaje de la Consola:**
```text
  File "/home/manu/Documentos/Clases/Proyecto Integrador/ClaimVision_Backend/src/modules/auth/infra/jwt/token_service.py", line 26, in generate
    return jwt.encode(
           ~~~~~~~~~~^
        to_encode,
        ...
  File "/usr/lib64/python3.14/json/encoder.py", line 182, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
                    f'is not JSON serializable')
TypeError: Object of type UUID is not JSON serializable
when serializing dict item 'usuario_id'
```

### Como se soluciono
* **Análisis de Causa Raíz:** En `UserTable`, el campo `usuario_id` (y opcionalmente `aseguradora_id`) se define como tipo `UUID(as_uuid=True)`. SQLAlchemy, al mapear el registro de base de datos a Python, devuelve objetos del tipo `uuid.UUID` nativos de Python. Al empaquetar estos datos en `TokenPayload` y pasarlos a `jose.jwt.encode` (que utiliza `json.dumps`), el serializador de JSON falla porque no sabe cómo codificar el objeto `UUID` nativo.
* **Refactorización Aplicada:** Se modificó la función de mapeo `_to_domain` en `AuthRepository` para convertir de manera explícita los campos `usuario_id` y `aseguradora_id` a cadenas de texto (`str(obj.campo)`) si estos no son `None`. Esto garantiza que los objetos de dominio manejen cadenas seguras y serializables para JSON.

---

## 7. ImportError: cannot import name 'AuthUser' from 'src.modules.auth.domain.models'
### Descripción del problema
* **Contexto/Acción:** Al intentar iniciar la aplicación (FastAPI/uvicorn).
* **Traceback/Mensaje de la Consola:**
```text
ImportError: cannot import name 'AuthUser' from 'src.modules.auth.domain.models'
```

### Como se soluciono
* **Análisis de Causa Raíz:** El modelo de dominio `AuthUser` en `src/modules/auth/domain/models.py` fue renombrado a `User`. Sin embargo, múltiples archivos en el módulo de Auth y en otros módulos seguían importando y utilizando el nombre antiguo `AuthUser`.
* **Refactorización Aplicada:** Se realizó una búsqueda y reemplazo en todos los puertos, repositorios y casos de uso de `AuthUser` a `User`, asegurando la consistencia del tipo de retorno e importaciones a lo largo del sistema (ej: en `auth_repository.py`, `ports.py`, `login_user.py`, `register_user.py`).

---

## 8. sqlalchemy.exc.InvalidRequestError: Table 'perfiles_clientes' is already defined
### Descripción del problema
* **Contexto/Acción:** Al importar las rutas y dependencias que cargaban modelos de bases de datos para el módulo aseguradora en el arranque del servidor.
* **Traceback/Mensaje de la Consola:**
```text
sqlalchemy.exc.InvalidRequestError: Table 'perfiles_clientes' is already defined for this MetaData instance. Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
```

### Como se soluciono
* **Análisis de Causa Raíz:** Durante el desarrollo modular por subentidades, la tabla `perfiles_clientes` fue definida tanto en el módulo de `cliente` (`cliente_profile_table.py`) como en el módulo de `aseguradora` (`perfil_cliente_table.py`) compartiendo el mismo nombre `__tablename__ = "perfiles_clientes"`. SQLAlchemy rastrea y asocia las tablas de una base de forma global (Metadata), por lo que declarar múltiples modelos bajo la misma tabla sin configuración previa arroja un error de redefinición de metadatos.
* **Refactorización Aplicada:** Se agregó el atributo `__table_args__ = {'extend_existing': True}` al modelo `PerfilClienteTable` dentro del módulo de aseguradora. Esto le indica al ORM que asocie este modelo a la tabla ya existente generada por el primer módulo que la declare durante el arranque, permitiendo convivir las definiciones en la misma metadata.

---

## 9. Importación cruzada entre módulos: ia_bridge y cliente/aseguradora
### Descripción del problema
* **Contexto/Acción:** Al implementar el flujo de creación de vehículos desde póliza OCR, se detectó que el módulo `cliente` necesitaba acceder a `OcrStructuredService` (de `ia_bridge`) y a `VehiculoAdapter`/`VehiculoModulePort` (de `aseguradora`). Esto potencialmente crea dependencias circulares o violaciones de capa si no se gestiona correctamente.
* **Causa Raíz:** El módulo `cliente` no tiene acceso directo a los servicios de `ia_bridge` ni a los puertos de `aseguradora` para crear vehículos. La solución requiere inyectar estas dependencias a través de `dependencies.py` en la capa de presentación, manteniendo el patrón de arquitectura hexagonal.
* **Refactorización Aplicada:**
  1. Se creó `CreateVehicleFromPoliza` en `cliente/application/` que depende de `OcrStructuredPort`, `VehiculoModulePort` y `ClienteRepositoryPort` (puertos abstractos).
  2. La inyección de dependencias concretas (`OcrStructuredService`, `VehiculoAdapter`, `ClienteRepository`) se realizó exclusivamente en `cliente_v1_dependencies.py`.
  3. Se aplicó el mismo patrón para `CreateVehiculoFromPoliza` en el módulo `aseguradora`.
  4. Los puertos se definieron en los módulos correspondientes (`ia_bridge/domain/ports.py`, `aseguradora/domain/ports/`) respetando la separación por contexto de negocio.

---

## 10. Manejo de content_type en uploads de imagen (INE)
### Descripción del problema
* **Contexto/Acción:** El endpoint `POST /api/v1/ocr/extract-ine` acepta tanto imágenes (JPG/PNG) como PDFs. El `content_type` del archivo subido puede variar según el navegador/cliente (`image/jpeg`, `image/jpg`, `image/png`, `application/pdf`).
* **Refactorización Aplicada:**
  1. Se validó el `content_type` contra un conjunto de tipos permitidos (`allowed_types`) en el endpoint del IA Service.
  2. Se propagó el `content_type` desde el Backend hacia el IA Service para que `ExtractIneUseCase` decida si usar `ImageOCRService` (Tesseract directo) o `OCRService` (PyMuPDF + fallback Tesseract).
  3. En `OcrStructuredService` del Backend, se pasó el `content_type` original del archivo al servicio de IA para mantener la compatibilidad con ambos formatos.

---

## 11. PyMuPDF OCR produce texto basura en PDFs escaneados de INE
### Descripción del problema
* **Contexto/Acción:** El endpoint `POST /api/v1/ocr/extract-ine` recibía un PDF escaneado de INE pero retornaba todos los campos vacíos.
* **Traceback/Mensaje de la Consola:** Sin traceback, el endpoint respondía 200 OK pero con strings vacíos en todos los campos.
* **Causa Raíz:** `PyMuPDFOCRService` usaba `page.get_pixmap(dpi=300)` para renderizar la página del PDF como imagen y pasarla a Tesseract. Sin embargo, PyMuPDF no renderiza correctamente las imágenes embebidas en PDFs escaneados, produciendo una imagen distorsionada que Tesseract no puede leer.
* **Refactorización Aplicada:**
  1. Se agregó un paso intermedio en `PyMuPDFOCRService`: extraer las imágenes embebidas del PDF directamente usando `doc.extract_image(xref)` en lugar de renderizar la página completa.
  2. El flujo de extracción ahora tiene 3 pasos: (1) texto directo → (2) imágenes embebidas → (3) renderizado de página como fallback.
  3. Se incrementó el DPI de renderizado de 300 a 400 para el caso fallback.
  4. Se cambiaron los campos `sexo`, `fecha_nacimiento`, `domicilio` y `clave_elector` en `IneExtractedResponse` a `Optional[str] = None` para manejar casos donde la LLM retorna `null`.

---

## 12. Validación de calidad de imagen para INE y Póliza
### Descripción del problema
* **Contexto/Acción:** El endpoint `POST /api/v1/ocr/extract-ine` aceptaba cualquier imagen/PDF sin validar calidad, resultando en extracción fallida cuando la imagen era borrosa, oscura o de baja resolución.
* **Causa Raíz:** No existía validación previa al OCR. Imágenes de baja calidad pasaban directamente al pipeline de extracción, produciendo resultados vacíos o incorrectos.

### Como se soluciono
* **Refactorización Aplicada:**
  1. Se creó el módulo `app/modules/ocr/infra/validation/` con:
     - `models.py`: Modelo `ValidationResult` con campos `is_valid`, `errors`, `warnings`, y métricas de imagen.
     - `image_validator.py`: Clase `ImageValidator` con métodos `validate_ine_image()` y `validate_poliza_pdf()` que verifican:
       - Resolución mínima (INE: 800x500, Póliza: 1000x700)
       - Nitidez (varianza Laplaciana > 50 para INE, > 30 para Póliza)
       - Brillo (rango 50-220 para INE, 60-220 para Póliza)
       - Aspecto (tolerancia 25%, advertencia pero no rechazo)
  2. Se integró la validación en `routes.py` antes de la extracción OCR.
  3. Se agregó check de calidad OCR en `ExtractIneUseCase` (mínimo 50 caracteres).
  4. Se mejoró el manejo de errores en `ia_bridge` para preservar mensajes del IA Service.
  5. Se documentó el estándar en `DOCUMENTACION_ESTANDARES_CAPTURA.md` para el frontend.
