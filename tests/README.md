# Tests del Sistema SIA

Esta carpeta contiene todas las pruebas del sistema organizadas por funcionalidad para facilitar el mantenimiento y la ejecución de tests específicos.

## 📁 Estructura de Tests

### 🔍 `/validation/`
Tests relacionados con validación de datos y formularios:
- `quick_validation_test.py` - Prueba rápida del sistema de validaciones
- `test_dni_implementation.py` - Test de implementación del campo DNI
- `test_dni_modal_integration.py` - Test de integración del modal DNI
- `test_manual_validation.py` - Test manual de validaciones de formulario
- `test_validation_function.py` - Test de funciones específicas de validación

### 🎨 `/ui/`
Tests de componentes de interfaz de usuario:
- `test_toast_colors.py` - Test de esquemas de colores para toasts
- `test_toast_components.py` - Test de componentes de notificación toast
- `test_toast_rendering.py` - Test de renderizado de toasts
- `test_modal_quick.py` - Test rápido de funcionalidad de modales
- `test_user_modal_fix.py` - Test de correcciones del modal de usuario
- `test_user_modal_validation.py` - Test de validaciones en modal de usuario

### 👥 `/users/`
Tests relacionados con funcionalidad de usuarios y perfiles:
- `test_create_user.py` - Test de creación de nuevos usuarios
- `test_get_user.py` - Test de obtención de datos de usuario
- `test_user_statistics.py` - Test de estadísticas de usuarios
- `test_profiles_layout.py` - Test de layout y diseño de perfiles

### ⚙️ `/system/`
Tests del sistema, componentes generales e integración:
- `test_components.py` - Test de componentes generales del sistema
- `test_data_table_refactor.py` - Test de refactorización de tablas de datos
- `test_dynamic_state.py` - Test de manejo de estado dinámico
- `test_fase3_imports.py` - Test de imports de implementación fase 3
- `test_import_fix.py` - Test de correcciones de importaciones
- `test_logging.py` - Test del sistema de logging

## 🚀 Cómo Ejecutar Tests

### Tests Individuales
```bash
# Ejecutar un test específico
python tests/validation/quick_validation_test.py
python tests/ui/test_toast_colors.py
python tests/system/test_logging.py
```

### Tests por Categoría
```bash
# Ejecutar todos los tests de validación
python -m pytest tests/validation/ -v

# Ejecutar todos los tests de UI
python -m pytest tests/ui/ -v

# Ejecutar todos los tests de usuarios
python -m pytest tests/users/ -v

# Ejecutar todos los tests de sistema
python -m pytest tests/system/ -v
```

### Todos los Tests
```bash
# Ejecutar toda la suite de tests
python -m pytest tests/ -v
```

### Con Filtros Específicos
```bash
# Solo tests que contengan "validation" en el nombre
pytest -k "validation" tests/

# Solo tests de toast
pytest -k "toast" tests/ui/

# Tests con salida detallada
pytest -v --tb=short tests/
```

## 🔧 Configuración y Requisitos

### Prerequisitos
Antes de ejecutar los tests, asegúrate de:

1. **Entorno Virtual Activado:**
   ```bash
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

2. **Dependencias Instaladas:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Base de Datos (si es necesario):**
   ```bash
   docker compose up -d  # Para tests que requieren BD
   ```

4. **Variables de Entorno:**
   Configurar archivo `.env` con las variables necesarias para testing.

### Estructura del Proyecto
Esta organización sigue las mejores prácticas:
- **Separación por funcionalidad** - Cada subcarpeta agrupa tests relacionados
- **Naming convention** - Prefijo `test_` para todos los archivos de test
- **Modularidad** - Tests independientes que pueden ejecutarse por separado
- **Escalabilidad** - Fácil adición de nuevas categorías de tests

## 📋 Tipos de Tests

### Tests de Validación (`/validation/`)
Verifican que las reglas de negocio y validaciones de entrada funcionen correctamente:
- Validación de formularios
- Reglas de DNI
- Integración de modales de validación

### Tests de UI (`/ui/`)
Aseguran que los componentes de interfaz se rendericen y funcionen correctamente:
- Sistema de notificaciones toast
- Modales y componentes interactivos
- Consistencia visual y funcional

### Tests de Usuarios (`/users/`)
Verifican la funcionalidad relacionada con gestión de usuarios:
- Operaciones CRUD de usuarios
- Estadísticas y métricas
- Layout y presentación de perfiles

### Tests de Sistema (`/system/`)
Pruebas de integración y componentes del núcleo del sistema:
- Componentes base y utilidades
- Sistema de logging
- Estado dinámico de la aplicación
- Correcciones e imports

## 🎯 Mejores Prácticas

1. **Ejecuta tests antes de hacer commit** para asegurar que no hay regresiones
2. **Agrupa tests relacionados** en la subcarpeta apropiada
3. **Usa nombres descriptivos** que expliquen qué se está probando
4. **Incluye tests tanto positivos como negativos** (casos de éxito y error)
5. **Mantén tests independientes** - cada test debe poder ejecutarse por separado

## 🔍 Debugging

Para debuggear tests que fallan:

```bash
# Ejecutar un test específico con máximo detalle
pytest tests/validation/test_dni_implementation.py -v -s --tb=long

# Parar en el primer error
pytest tests/ -x

# Mostrar todas las salidas print()
pytest tests/ -s
```

## 📈 Cobertura

Para generar reportes de cobertura de código:

```bash
# Instalar coverage si no está instalado
pip install coverage

# Ejecutar tests con cobertura
coverage run -m pytest tests/

# Generar reporte
coverage report -m
coverage html  # Genera reporte HTML en htmlcov/
```

Esta estructura de tests organizada facilita el mantenimiento, la ejecución selectiva de pruebas y el desarrollo colaborativo del sistema SIA.