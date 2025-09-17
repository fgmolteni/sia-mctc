"""
Utilidades para trabajar con los modelos de validación en Reflex.

Este módulo proporciona funciones de ayuda para integrar los modelos Pydantic
con la aplicación Reflex, incluyendo conversión de datos, manejo de errores
y validación en tiempo real.
"""

from typing import Dict, Any, List, Tuple
from pydantic import ValidationError
import pandas as pd



def validate_and_convert(model_class, data: Dict[str, Any]) -> Tuple[bool, Any, List[str]]:
    """
    Valida datos usando un modelo Pydantic y retorna resultado estructurado.
    
    Args:
        model_class: Clase del modelo Pydantic a usar
        data: Diccionario con los datos a validar
        
    Returns:
        Tuple con (es_válido, modelo_o_None, lista_de_errores)
        
    Ejemplo:
        is_valid, user, errors = validate_and_convert(User, user_data)
        if not is_valid:
            print("Errores:", errors)
    """
    try:
        validated_model = model_class(**data)
        return True, validated_model, []
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field = error.get('loc', ['unknown'])[0]
            message = error.get('msg', 'Error de validación')
            error_messages.append(f"{field}: {message}")
        return False, None, error_messages
    except Exception as e:
        return False, None, [f"Error inesperado: {str(e)}"]


def validate_dataframe_rows(model_class, df: pd.DataFrame) -> Tuple[List[Any], List[Dict]]:
    """
    Valida múltiples filas de un DataFrame usando un modelo Pydantic.
    
    Args:
        model_class: Clase del modelo Pydantic
        df: DataFrame con los datos
        
    Returns:
        Tuple con (lista_de_modelos_válidos, lista_de_errores_por_fila)
        
    Ejemplo:
        valid_users, errors = validate_dataframe_rows(User, users_df)
    """
    valid_models = []
    errors_by_row = []
    
    for idx, row in df.iterrows():
        row_data = row.to_dict()
        is_valid, model, errors = validate_and_convert(model_class, row_data)
        
        if is_valid:
            valid_models.append(model)
            errors_by_row.append(None)
        else:
            errors_by_row.append({
                'row_index': idx,
                'errors': errors,
                'data': row_data
            })
    
    return valid_models, [e for e in errors_by_row if e is not None]


def get_model_fields_info(model_class) -> Dict[str, Dict[str, Any]]:
    """
    Obtiene información sobre los campos de un modelo Pydantic.
    
    Args:
        model_class: Clase del modelo Pydantic
        
    Returns:
        Diccionario con información de cada campo
        
    Ejemplo:
        fields_info = get_model_fields_info(User)
        print(fields_info['nombre']['required'])  # True
    """
    fields_info = {}
    
    for field_name, field_info in model_class.model_fields.items():
        fields_info[field_name] = {
            'required': field_info.is_required(),
            'type': str(field_info.annotation),
            'default': field_info.default if field_info.default is not None else None,
            'description': field_info.description
        }
    
    return fields_info


def create_form_validation_rules(model_class) -> Dict[str, Dict[str, Any]]:
    """
    Genera reglas de validación para formularios de Reflex basadas en modelos Pydantic.
    
    Args:
        model_class: Clase del modelo Pydantic
        
    Returns:
        Diccionario con reglas de validación para cada campo
        
    Ejemplo:
        rules = create_form_validation_rules(User)
        # Usar en componentes de formulario de Reflex
    """
    validation_rules = {}
    fields_info = get_model_fields_info(model_class)
    
    for field_name, field_data in fields_info.items():
        rules = {
            'required': field_data['required'],
            'field_type': field_data['type'],
            'description': field_data['description']
        }
        
        # Agregar reglas específicas basadas en el modelo
        if field_name in ['nombre', 'apellido']:
            rules.update({
                'min_length': 1,
                'max_length': 100,
                'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
                'pattern_message': 'Solo se permiten letras y espacios'
            })
        
        elif field_name == 'dni':
            rules.update({
                'min_length': 7,
                'max_length': 8,
                'pattern': r'^\d{7,8}$',
                'pattern_message': 'DNI debe tener 7 u 8 dígitos'
            })
        
        elif field_name == 'patente':
            rules.update({
                'pattern': r'^([A-Z]{3}\d{3}|[A-Z]{2}\d{3}[A-Z]{2}|\d{3}[A-Z]{3})$',
                'pattern_message': 'Formato de patente inválido'
            })
        
        elif field_name == 'nombre_usuario':
            rules.update({
                'min_length': 3,
                'max_length': 50,
                'pattern': r'^[a-zA-Z0-9_-]+$',
                'pattern_message': 'Solo letras, números, guiones y guiones bajos'
            })
        
        elif field_name in ['consumo', 'distancia_total_km', 'combustible_estimado_lts']:
            rules.update({
                'min_value': 0,
                'input_type': 'number',
                'step': 0.01
            })
        
        validation_rules[field_name] = rules
    
    return validation_rules


def format_validation_errors_for_ui(errors: List[str]) -> Dict[str, str]:
    """
    Formatea errores de validación para mostrar en la UI de Reflex.
    
    Args:
        errors: Lista de errores de validación
        
    Returns:
        Diccionario con errores agrupados por campo
        
    Ejemplo:
        formatted_errors = format_validation_errors_for_ui(validation_errors)
        # Mostrar errores en componentes específicos
    """
    formatted_errors = {}
    
    for error in errors:
        if ':' in error:
            field, message = error.split(':', 1)
            formatted_errors[field.strip()] = message.strip()
        else:
            formatted_errors['general'] = error
    
    return formatted_errors


def sanitize_input_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitiza datos de entrada antes de la validación.
    
    Args:
        data: Diccionario con datos a sanitizar
        
    Returns:
        Diccionario con datos sanitizados
        
    Ejemplo:
        clean_data = sanitize_input_data(form_data)
        is_valid, model, errors = validate_and_convert(User, clean_data)
    """
    sanitized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            # Remover espacios extra
            value = value.strip()
            
            # Convertir strings vacíos a None para campos opcionales
            if value == '':
                value = None
            
            # Sanitización específica por campo
            elif key in ['nombre', 'apellido']:
                # Capitalizar nombres
                value = value.title()
            
            elif key == 'nombre_usuario':
                # Convertir a minúsculas
                value = value.lower()
            
            elif key == 'dni':
                # Remover puntos y espacios del DNI
                import re
                value = re.sub(r'[.\s-]', '', value)
            
            elif key == 'patente':
                # Convertir a mayúsculas y remover espacios
                value = value.upper().replace(' ', '')
        
        elif isinstance(value, (int, float)) and value == 0:
            # Convertir 0 a None para campos opcionales que no permiten 0
            if key in ['consumo', 'distancia_total_km', 'combustible_estimado_lts']:
                value = None
        
        sanitized[key] = value
    
    return sanitized


def convert_model_to_dict(model_instance, include_none: bool = False) -> Dict[str, Any]:
    """
    Convierte una instancia de modelo Pydantic a diccionario para uso en Reflex.
    
    Args:
        model_instance: Instancia del modelo Pydantic
        include_none: Si incluir campos con valor None
        
    Returns:
        Diccionario con los datos del modelo
        
    Ejemplo:
        user_dict = convert_model_to_dict(user_model)
        # Usar para actualizar estado en Reflex
    """
    if include_none:
        return model_instance.model_dump()
    else:
        return model_instance.model_dump(exclude_none=True)


def batch_validate(model_class, data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Valida múltiples elementos en lote y retorna estadísticas.
    
    Args:
        model_class: Clase del modelo Pydantic
        data_list: Lista de diccionarios con datos
        
    Returns:
        Diccionario con estadísticas de validación
        
    Ejemplo:
        stats = batch_validate(Agent, agents_data)
        print(f"Válidos: {stats['valid_count']}")
        print(f"Errores: {stats['error_count']}")
    """
    valid_models = []
    invalid_items = []
    
    for idx, data in enumerate(data_list):
        is_valid, model, errors = validate_and_convert(model_class, data)
        
        if is_valid:
            valid_models.append(model)
        else:
            invalid_items.append({
                'index': idx,
                'data': data,
                'errors': errors
            })
    
    return {
        'valid_count': len(valid_models),
        'error_count': len(invalid_items),
        'valid_models': valid_models,
        'invalid_items': invalid_items,
        'success_rate': len(valid_models) / len(data_list) * 100 if data_list else 0
    }