# Modelos de Validación SIA-MCTC

Este módulo contiene los modelos Pydantic para validación de datos del Sistema Interno de Administración (SIA) del Ministerio de Ciencia y Tecnología.

## Estructura

```
sia/models/
├── __init__.py          # Exports principales del módulo
├── validation.py        # Modelos Pydantic principales
├── utils.py            # Utilidades para trabajar con los modelos
├── examples.py         # Ejemplos de uso
└── README.md           # Esta documentación
```

## Modelos Disponibles

### Modelos Principales
- **User**: Validación para tabla `usuarios`
- **Agent**: Validación para tabla `agentes`  
- **Vehicle**: Validación para tabla `vehiculos`
- **Expedient**: Validación para tabla `expedientes`

### Modelos de Operación
- **UserCreate**: Para crear nuevos usuarios
- **UserUpdate**: Para actualizar usuarios existentes
- **AgentCreate**: Para crear nuevos agentes
- **VehicleCreate**: Para crear nuevos vehículos

## Validaciones Incluidas

### Específicas del Dominio
- **DNI**: Formato argentino (7-8 dígitos)
- **Patente**: Formatos argentinos (ABC123, AB123CD, 123ABC)
- **Nombres**: Solo letras y espacios, capitalización automática
- **Consumo**: Valores razonables para vehículos
- **Fechas**: Fechas de regreso posteriores a salida

### Generales
- Longitudes de campo según esquema SQL
- Campos requeridos vs opcionales
- Tipos de datos correctos
- Validación de roles y enums

## Uso Básico

```python
from sia.models import User, validate_and_convert

# Validar datos de usuario
user_data = {
    "nombre": "juan",
    "apellido": "pérez", 
    "nombre_usuario": "jperez",
    "hash_contrasena": "hash_aquí",
    "rol": "usuario"
}

is_valid, user, errors = validate_and_convert(User, user_data)
if not is_valid:
    print("Errores:", errors)
else:
    print(f"Usuario válido: {user.nombre} {user.apellido}")
```

## Integración con Reflex

```python
from sia.models import create_form_validation_rules, sanitize_input_data

# Generar reglas para formularios
validation_rules = create_form_validation_rules(Agent)

# Sanitizar datos de formulario antes de validar
clean_data = sanitize_input_data(form_data)
is_valid, agent, errors = validate_and_convert(Agent, clean_data)
```

## Dependencias

Asegúrate de tener instalado:
```bash
pip install pydantic email-validator
```

## Archivos de Ejemplo

Revisa `examples.py` para ver casos de uso completos y ejemplos de errores de validación comunes.