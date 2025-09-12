# Crear Usuario Administrador - SIA-MCTC

Este documento explica cómo crear el usuario administrador inicial para el sistema SIA-MCTC.

## Resumen

Se ha creado un script automatizado que:
1. ✅ Verifica la conexión a PostgreSQL
2. ✅ Aplica las migraciones necesarias (campos email y DNI)
3. ✅ Crea el usuario administrador con credenciales predefinidas
4. ✅ Verifica que todo se creó correctamente

## Credenciales del Usuario Administrador

- **Username:** `adm`
- **Password:** `adm1234`
- **Email:** `admin@sia-mctc.local`
- **DNI:** `12345678`
- **Rol:** `admin`

## Pasos para Ejecutar

### 1. Preparar el Entorno

```bash
# Iniciar PostgreSQL (si no está corriendo)
docker compose up -d

# Verificar que PostgreSQL esté activo
docker ps
```

### 2. Ejecutar el Script de Creación

```bash
# Desde el directorio raíz del proyecto
python setup_admin_user.py
```

### 3. Verificar la Creación

El script incluye verificación automática, pero puedes confirmar manualmente:

```bash
# Conectar a PostgreSQL
docker exec -it sia-mctc-db-1 psql -U user_sia -d db_sia

# Verificar usuario creado
SELECT id, nombre, apellido, nombre_usuario, email, dni, rol, fecha_creacion 
FROM usuarios WHERE nombre_usuario = 'adm';
```

## Scripts Disponibles

### Script Principal (Recomendado)
- **`setup_admin_user.py`** - Script completo con verificaciones y migraciones automáticas

### Scripts de Soporte
- **`create_admin_user.py`** - Versión detallada con logging extenso
- **`create_admin_simple.py`** - Versión simplificada para debugging
- **`check_admin_user.py`** - Solo verificar usuarios existentes
- **`test_db_connection.py`** - Solo probar conexión a base de datos

## Solución de Problemas

### Error: No se puede conectar a PostgreSQL
```bash
# Verificar estado de Docker
docker ps

# Iniciar servicios si están detenidos
docker compose up -d

# Verificar logs si hay problemas
docker compose logs db
```

### Error: Variables de entorno no definidas
Verifica que existe el archivo `.env` con:
```
POSTGRES_USER=user_sia
POSTGRES_PASSWORD=password_sia
POSTGRES_DB=db_sia
DATABASE_URL=postgresql://user_sia:password_sia@localhost:5432/db_sia
```

### Error: Usuario ya existe
El script detecta usuarios administradores existentes y pregunta si continuar. Para forzar la creación sin preguntar, modifica el script.

### Error: Campos de tabla faltantes
El script aplica automáticamente las migraciones necesarias:
- Agrega campo `email` a la tabla `usuarios`
- Agrega campo `dni` a la tabla `usuarios`
- Crea índices únicos correspondientes

## Verificación Manual del Sistema

### 1. Estructura de Base de Datos
```sql
-- Verificar estructura de tabla usuarios
\d usuarios

-- Debe mostrar columnas: id, nombre, apellido, nombre_usuario, email, dni, hash_contrasena, rol, fecha_creacion
```

### 2. Usuario Administrador
```sql
-- Verificar usuario administrador
SELECT * FROM usuarios WHERE rol = 'admin';

-- Verificar unicidad de email y dni
SELECT email, COUNT(*) FROM usuarios GROUP BY email HAVING COUNT(*) > 1;
SELECT dni, COUNT(*) FROM usuarios WHERE dni IS NOT NULL GROUP BY dni HAVING COUNT(*) > 1;
```

### 3. Función de Login
```python
# Probar autenticación (en Python)
from components.db_users import verify_user

success, message, user = verify_user("adm", "adm1234")
print(f"Login exitoso: {success}")
if success:
    print(f"Usuario: {user.nombre} {user.apellido} - {user.rol}")
```

## Seguridad Post-Instalación

### 1. Cambiar Contraseña (IMPORTANTE)
```python
# Usar la aplicación web o crear script para cambiar contraseña
from components.db_users import update_user
from sia.models.validation import UserUpdate

# Actualizar con nueva contraseña segura
update_data = UserUpdate(contrasena="nueva_contrasena_segura")
update_user(user_id, update_data)
```

### 2. Configurar Email Real
```python
# Actualizar email del administrador
update_data = UserUpdate(email="admin_real@ministerio.gov.ar")
update_user(user_id, update_data)
```

### 3. Configurar DNI Real
```python
# Actualizar DNI del administrador
update_data = UserUpdate(dni=12345678)  # DNI real
update_user(user_id, update_data)
```

## Notas Técnicas

### Validaciones Implementadas
- **Password:** Mínimo 6 caracteres, debe incluir letras y números
- **Email:** Formato válido y único en el sistema
- **DNI:** Rango válido argentino (1.000.000 - 99.999.999) y único
- **Username:** Mínimo 3 caracteres, solo letras, números, puntos, guiones

### Encriptación
- Las contraseñas se encriptan usando **bcrypt** antes de almacenarse
- El hash se genera con salt aleatorio para máxima seguridad

### Base de Datos
- **PostgreSQL 15+** con extensiones estándar
- **SQLAlchemy** como ORM para interacción con base de datos
- **Migraciones automáticas** para campos email y DNI

### Logging
- Eventos de seguridad registrados en `/logs/sia_security.log`
- Eventos de base de datos en `/logs/sia_database.log`
- Configuración de logging en `components/logging/`

## Estado del Sistema

✅ **Completado:**
- Función `create_user()` con validación Pydantic
- Encriptación bcrypt de contraseñas
- Validaciones de unicidad (email, username, DNI)
- Sistema de logging de seguridad
- Migraciones automáticas de esquema
- Scripts de verificación y diagnóstico

🔧 **Para Usar:**
1. Ejecutar `python setup_admin_user.py`
2. Acceder a la aplicación web con credenciales `adm / adm1234`
3. Cambiar contraseña y email en primer acceso
4. Comenzar a usar el sistema SIA-MCTC

---

**Autor:** Sistema SIA-MCTC  
**Fecha:** Septiembre 2024  
**Versión:** 1.0