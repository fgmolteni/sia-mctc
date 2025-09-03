"""
Módulo de modelos de datos para el Sistema Interno de Administración (SIA).

Este módulo contiene los modelos Pydantic para validación de datos
que corresponden a las tablas de la base de datos PostgreSQL.
"""

from .validation import (
    User, Agent, Vehicle, Expedient,
    UserCreate, UserUpdate, AgentCreate, VehicleCreate
)
from .utils import (
    validate_and_convert,
    validate_dataframe_rows,
    get_model_fields_info,
    create_form_validation_rules,
    format_validation_errors_for_ui,
    sanitize_input_data,
    convert_model_to_dict,
    batch_validate
)

__all__ = [
    # Modelos de validación principales
    "User",
    "Agent", 
    "Vehicle",
    "Expedient",
    
    # Modelos de creación y actualización
    "UserCreate",
    "UserUpdate", 
    "AgentCreate",
    "VehicleCreate",
    
    # Utilidades
    "validate_and_convert",
    "validate_dataframe_rows", 
    "get_model_fields_info",
    "create_form_validation_rules",
    "format_validation_errors_for_ui",
    "sanitize_input_data",
    "convert_model_to_dict",
    "batch_validate"
]