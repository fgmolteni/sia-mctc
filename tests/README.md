# Testing Suite para SIA-MCTC

## Descripción

Esta suite de pruebas sigue **metodología TDD estricta** para los componentes de la página de usuarios de SIA-MCTC. Las pruebas están diseñadas para **FALLAR INICIALMENTE** (Red phase) y guiar el desarrollo hacia la implementación correcta.

## Estructura de Testing

```
tests/
├── __init__.py                     # Paquete de tests
├── conftest.py                     # Configuración global pytest + fixtures base
├── models.py                       # Modelos Pydantic para datos de prueba
├── fixtures.py                     # Fixtures de datos validados
├── components/                     # Tests de componentes UI
│   ├── __init__.py
│   ├── test_stat_card.py          # Pruebas para tarjetas de estadísticas  
│   ├── test_role_badge.py         # Pruebas para badges de roles
│   ├── test_status_badge.py       # Pruebas para badges de estado
│   ├── test_data_table.py         # Pruebas para tabla de datos
│   └── test_search_filters.py     # Pruebas para filtros de búsqueda
├── pages/                          # Tests de páginas y estado
│   ├── __init__.py
│   └── test_user_state.py         # Pruebas para UserState class
└── README.md                       # Esta documentación
```

## Componentes Probados

### 1. **stat_card** (`test_stat_card.py`)
- ✅ Renderizado con props básicos (título, valor, ícono)
- ✅ Manejo de `icon_color` personalizado y por defecto
- ✅ Múltiples configuraciones y casos edge
- ✅ Estructura de componente y estilos correctos
- ✅ Validación de parámetros obligatorios

### 2. **role_badge** (`test_role_badge.py`)
- ✅ Esquemas de colores por rol (admin, manager, employee, default)
- ✅ Valores por defecto y roles inexistentes
- ✅ Propiedades de estilo y **kwargs adicionales
- ✅ Validación de tipos Literal y manejo de texto especial

### 3. **status_badge** (`test_status_badge.py`)
- ✅ Estados con dots opcionales (`show_dot=True/False`)
- ✅ Esquemas de colores para todos los estados
- ✅ Renderizado condicional (hstack vs badge)
- ✅ Propiedades del dot y casos edge

### 4. **data_table** (`test_data_table.py`)
- ✅ Estructura básica de tabla con headers
- ✅ Funciones de renderizado personalizadas por columna
- ✅ Contador de elementos y columna de acciones
- ✅ Mapeo automático de headers con datos
- ✅ Casos edge (datos vacíos, headers faltantes)

### 5. **search_filters** (`test_search_filters.py`)
- ✅ Estructura responsive (input 60% + selects 40%)
- ✅ Opciones correctas para roles y estados
- ✅ Propiedades de estilo y espaciado
- ✅ Componente autónomo sin parámetros externos

### 6. **UserState** (`test_user_state.py`)
- ✅ Herencia de `rx.State` y inicialización correcta
- ✅ Carga de datos estáticos con `load_users()`
- ✅ Validación con modelos Pydantic
- ✅ Consistencia de datos y tipos correctos
- ✅ Preparación para integración futura con BD

## Modelos Pydantic

### `User`
```python
class User(BaseModel):
    name: str                    # Formato: "Nombre Apellido"
    email: EmailStr              # Email válido
    role: Literal["Administrador", "Manager", "Empleado"]
    area: str                    # Área de trabajo
    status: Literal["Activo", "Inactivo"]
    permissions: str             # Formato: "N permisos"
    attributes: str              # Formato: "N atributos"  
    last_access: str            # Formato: "dd/mm/yyyy"
```

### `UserStatistics`
```python
class UserStatistics(BaseModel):
    total_users: int
    active_users: int
    administrators: int
    managers: int
    employees: int
```

## Fixtures Principales

- **`valid_user_data`**: Datos válidos para pruebas exitosas
- **`invalid_user_data`**: Datos inválidos para probar validaciones
- **`sample_users_list`**: Lista de 4 usuarios para pruebas de tabla
- **`validated_users`**: Usuarios validados con Pydantic
- **`stat_card_test_cases`**: Casos de prueba para tarjetas estadísticas
- **`role_badge_test_cases`**: Esquemas de colores por rol
- **`status_badge_test_cases`**: Estados con dots opcionales

## Ejecutar Pruebas

### Todas las pruebas
```bash
pytest
```

### Por categoría (usando marcadores)
```bash
pytest -m component        # Solo componentes UI
pytest -m state           # Solo pruebas de estado
pytest -m unit            # Solo pruebas unitarias
pytest -m integration     # Solo pruebas de integración
```

### Componente específico
```bash
pytest tests/components/test_stat_card.py
pytest tests/pages/test_user_state.py
```

### Con output detallado
```bash
pytest -v --tb=short
```

## Metodología TDD

### Fase Actual: RED 🔴
**Todas las pruebas FALLARÁN inicialmente** porque:

1. **Componentes pueden no existir** o tener implementación incompleta
2. **Funcionalidad no implementada** según especificaciones de las pruebas  
3. **Integración con Pydantic** no completada
4. **Validaciones** no implementadas
5. **Estructura de datos** no conforme con modelos

### Próximos Pasos: GREEN 🟢
1. **Implementar funcionalidad mínima** para que cada prueba pase
2. **Ajustar componentes** según los assertions de las pruebas
3. **Validar con Pydantic** los datos de UserState  
4. **Aplicar estilos** según propiedades esperadas en las pruebas
5. **Manejar casos edge** definidos en las pruebas

### Fase Final: REFACTOR 🔵
1. **Optimizar código** manteniendo pruebas verdes
2. **Eliminar duplicación** entre componentes
3. **Mejorar performance** si es necesario
4. **Documentar** funcionalidades implementadas

## Configuración Pytest

El archivo `pytest.ini` define:
- **Marcadores personalizados**: `unit`, `integration`, `component`, `state`, `slow`
- **Configuración de output**: verbose, colores, formato de traceback
- **Filtros de warnings**: ignora deprecation warnings de dependencias

## Mocks y Fixtures

- **`mock_reflex_imports`**: Auto-fixture que mockea componentes Reflex
- **`mock_reflex_state`**: Mock para estados de Reflex
- **`sample_database_connection`**: Mock para conexión a BD
- **Fixtures de datos**: Proporcionan datos estructurados y validados

## Casos de Prueba Especiales

### Edge Cases Cubiertos
- ✅ Datos vacíos y listas vacías
- ✅ Texto con caracteres especiales y acentos
- ✅ Valores muy largos que podrían romper layout  
- ✅ Parámetros faltantes y tipos incorrectos
- ✅ Estados inexistentes con fallback a defaults

### Integración con Pydantic
- ✅ Validación automática de estructura de datos
- ✅ Manejo de errores de validación  
- ✅ Conversión de tipos automática
- ✅ Schemas de ejemplo para documentación

## Contribuir

Al agregar nuevas pruebas:

1. **Sigue TDD estricto**: Escribe prueba → Falla → Implementa → Pasa
2. **Usa marcadores apropiados**: `@pytest.mark.component`, `@pytest.mark.state`
3. **Incluye documentación**: Explica qué debe fallar y por qué
4. **Valida con Pydantic**: Usa modelos para datos estructurados
5. **Cubre edge cases**: Incluye casos límite y manejo de errores

La suite de pruebas es la **especificación viva** del comportamiento esperado. Cada prueba representa un requisito específico que debe cumplir la implementación.