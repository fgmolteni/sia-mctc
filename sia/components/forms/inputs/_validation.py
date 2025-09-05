"""
Utilidades de validación client-side para formularios.

Este módulo proporciona funciones de validación basadas en las reglas
definidas en los modelos Pydantic, para ofrecer retroalimentación 
inmediata al usuario sin comprometer las validaciones server-side.
"""

import re
from typing import Dict, Any


def get_user_validation_rules() -> Dict[str, Dict[str, Any]]:
    """
    Reglas de validación para campos de usuario basadas en los modelos Pydantic.
    
    Returns:
        Diccionario con reglas para cada campo
    """
    return {
        'nombre': {
            'min_length': 1,
            'max_length': 100,
            'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
            'pattern_name': 'nombre',
            'helper_text': 'Solo letras y espacios (1-100 caracteres)',
            'auto_transform': 'title'
        },
        'apellido': {
            'min_length': 1,
            'max_length': 100,
            'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
            'pattern_name': 'apellido',
            'helper_text': 'Solo letras y espacios (1-100 caracteres)',
            'auto_transform': 'title'
        },
        'nombre_usuario': {
            'min_length': 3,
            'max_length': 50,
            'pattern': r'^[a-zA-Z0-9_.-]+$',
            'pattern_name': 'nombre de usuario',
            'helper_text': 'Letras, números, guiones y puntos (3-50 caracteres)',
            'auto_transform': 'lowercase',
            'unique_check': True
        },
        'email': {
            'min_length': 5,
            'max_length': 255,
            'email': True,
            'helper_text': 'Email válido (5-255 caracteres)',
            'auto_transform': 'lowercase',
            'unique_check': True
        },
        'dni': {
            'min_length': 7,
            'max_length': 8,
            'pattern': r'^\d{7,8}$',
            'pattern_name': 'DNI',
            'helper_text': 'DNI argentino sin puntos (7-8 dígitos)',
            'unique_check': True,
            'optional': True,
            'custom_validation': 'dni_argentino'
        },
        'contrasena': {
            'password': True,
            'min_length': 6,
            'helper_text': 'Al menos 6 caracteres, una letra y un número'
        }
    }


def get_agent_validation_rules() -> Dict[str, Dict[str, Any]]:
    """
    Reglas de validación para campos de agente.
    
    Returns:
        Diccionario con reglas para cada campo
    """
    return {
        'nombre': {
            'min_length': 1,
            'max_length': 100,
            'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
            'pattern_name': 'nombre',
            'helper_text': 'Solo letras y espacios (1-100 caracteres)',
            'auto_transform': 'title'
        },
        'apellido': {
            'min_length': 1,
            'max_length': 100,
            'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
            'pattern_name': 'apellido',
            'helper_text': 'Solo letras y espacios (1-100 caracteres)',
            'auto_transform': 'title'
        },
        'dni': {
            'min_length': 7,
            'max_length': 8,
            'pattern': r'^\d{7,8}$',
            'pattern_name': 'DNI',
            'helper_text': 'DNI argentino sin puntos (7-8 dígitos)',
            'unique_check': True
        },
        'cargo': {
            'max_length': 100,
            'helper_text': 'Cargo del agente (máximo 100 caracteres)',
            'auto_transform': 'title',
            'optional': True
        },
        'categoria': {
            'max_length': 50,
            'helper_text': 'Categoría del agente (máximo 50 caracteres)',
            'auto_transform': 'title',
            'optional': True
        }
    }


def get_vehicle_validation_rules() -> Dict[str, Dict[str, Any]]:
    """
    Reglas de validación para campos de vehículo.
    
    Returns:
        Diccionario con reglas para cada campo
    """
    return {
        'marca': {
            'min_length': 1,
            'max_length': 100,
            'pattern': r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\.]+$',
            'pattern_name': 'marca',
            'helper_text': 'Marca del vehículo (1-100 caracteres)',
            'auto_transform': 'title'
        },
        'modelo': {
            'min_length': 1,
            'max_length': 100,
            'pattern': r'^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-\.]+$',
            'pattern_name': 'modelo',
            'helper_text': 'Modelo del vehículo (1-100 caracteres)',
            'auto_transform': 'title'
        },
        'patente': {
            'min_length': 6,
            'max_length': 7,
            'helper_text': 'Patente argentina (ABC123 o AB123CD)',
            'auto_transform': 'uppercase',
            'unique_check': True,
            'custom_validation': 'patente_argentina'
        },
        'consumo': {
            'min_value': 0.1,
            'max_value': 50.0,
            'helper_text': 'Consumo en L/100km (0.1 - 50.0)',
            'numeric': True,
            'optional': True
        }
    }


def validate_patente_argentina(patente: str) -> tuple[bool, str]:
    """
    Valida formato de patente argentina.
    
    Args:
        patente: Patente a validar
        
    Returns:
        Tupla con (es_válida, mensaje_error)
    """
    if not patente:
        return False, "La patente no puede estar vacía"
    
    patente_clean = patente.strip().upper().replace(' ', '')
    
    # Patente antigua: 3 letras + 3 números (ej: ABC123)
    old_format = re.match(r'^[A-Z]{3}\d{3}$', patente_clean)
    
    # Patente nueva: 2 letras + 3 números + 2 letras (ej: AB123CD)
    new_format = re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', patente_clean)
    
    # Patente de motos: 3 números + 3 letras (ej: 123ABC)
    moto_format = re.match(r'^\d{3}[A-Z]{3}$', patente_clean)
    
    if not (old_format or new_format or moto_format):
        return False, "Formato inválido (ABC123, AB123CD o 123ABC)"
    
    return True, ""


def validate_dni_argentino(dni: str) -> tuple[bool, str]:
    """
    Valida formato de DNI argentino.
    
    Args:
        dni: DNI a validar
        
    Returns:
        Tupla con (es_válido, mensaje_error)
    """
    if not dni:
        return False, "El DNI no puede estar vacío"
    
    # Remover puntos y espacios si los hay
    dni_clean = re.sub(r'[.\s-]', '', dni.strip())
    
    # El DNI debe tener entre 7 y 8 dígitos
    if not re.match(r'^\d{7,8}$', dni_clean):
        return False, "DNI debe tener 7-8 dígitos numéricos"
    
    # Verificar que no sea un DNI obviamente inválido
    dni_num = int(dni_clean)
    if dni_num < 1000000 or dni_num > 99999999:
        return False, "DNI fuera del rango válido"
    
    return True, ""


def apply_auto_transform(value: str, transform_type: str) -> str:
    """
    Aplica transformación automática al texto.
    
    Args:
        value: Valor a transformar
        transform_type: Tipo de transformación
        
    Returns:
        Valor transformado
    """
    if not value:
        return value
    
    if transform_type == 'lowercase':
        return value.lower()
    elif transform_type == 'uppercase':
        return value.upper()
    elif transform_type == 'title':
        return value.title()
    
    return value


def validate_field_value(field_name: str, value: str, validation_rules: Dict[str, Dict[str, Any]] = None) -> tuple[bool, str]:
    """
    Valida un campo específico usando las reglas definidas.
    
    Args:
        field_name: Nombre del campo a validar
        value: Valor a validar (puede ser None o str)
        validation_rules: Reglas de validación (usa las de usuario por defecto)
        
    Returns:
        Tupla con (es_válido, mensaje_error)
    """
    if validation_rules is None:
        validation_rules = get_user_validation_rules()
    
    if field_name not in validation_rules:
        return True, ""
    
    # Manejar valores None o vacíos
    if value is None:
        value = ""
    
    value_str = str(value).strip()
    rules = validation_rules[field_name]
    
    # Si el campo es opcional y está vacío, es válido
    if rules.get('optional', False) and not value_str:
        return True, ""
    
    # Si el campo es requerido y está vacío
    if not rules.get('optional', False) and not value_str:
        field_display = _get_field_display_name(field_name)
        return False, f"El {field_display} es obligatorio"
    
    # Validación de longitud mínima
    if 'min_length' in rules:
        if len(value_str) < rules['min_length']:
            field_display = _get_field_display_name(field_name)
            return False, f"El {field_display} debe tener al menos {rules['min_length']} caracteres"
    
    # Validación de longitud máxima
    if 'max_length' in rules:
        if len(value_str) > rules['max_length']:
            field_display = _get_field_display_name(field_name)
            return False, f"El {field_display} no puede exceder {rules['max_length']} caracteres"
    
    # Validación de patrón regex (antes de validaciones específicas)
    if 'pattern' in rules:
        if not re.match(rules['pattern'], value_str):
            return False, _get_pattern_error_message(field_name, rules)
    
    # Validación de email
    if rules.get('email', False):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value_str):
            return False, "El email no tiene un formato válido"
    
    # Validación de password
    if rules.get('password', False):
        return _validate_password(value, rules)
    
    # Validaciones personalizadas
    if 'custom_validation' in rules:
        custom_type = rules['custom_validation']
        if custom_type == 'dni_argentino':
            # Para DNI opcional, si está vacío ya pasó la validación anterior
            if value_str:
                return validate_dni_argentino(value_str)
        elif custom_type == 'patente_argentina':
            return validate_patente_argentina(value_str)
    
    return True, ""


def _get_field_display_name(field_name: str) -> str:
    """Obtiene el nombre de display del campo en español."""
    display_names = {
        'nombre': 'nombre',
        'apellido': 'apellido', 
        'nombre_usuario': 'nombre de usuario',
        'email': 'email',
        'dni': 'DNI',
        'contrasena': 'contraseña',
        'cargo': 'cargo',
        'categoria': 'categoría',
        'marca': 'marca',
        'modelo': 'modelo',
        'patente': 'patente',
        'consumo': 'consumo'
    }
    return display_names.get(field_name, field_name)


def _get_pattern_error_message(field_name: str, rules: Dict[str, Any]) -> str:
    """Obtiene el mensaje de error específico para cada campo."""
    error_messages = {
        'nombre': 'El nombre debe contener solo letras y espacios',
        'apellido': 'El apellido debe contener solo letras y espacios',
        'nombre_usuario': 'El nombre de usuario solo puede contener letras, números, guiones y puntos',
        'dni': 'El DNI debe tener entre 7 y 8 dígitos',
        'marca': 'La marca solo puede contener letras, números, espacios, guiones y puntos',
        'modelo': 'El modelo solo puede contener letras, números, espacios, guiones y puntos'
    }
    
    return error_messages.get(field_name, f"Formato de {_get_field_display_name(field_name)} inválido")


def _validate_password(password: str, rules: Dict[str, Any]) -> tuple[bool, str]:
    """Valida una contraseña según las reglas definidas."""
    min_length = rules.get('min_length', 6)
    
    if len(password) < min_length:
        return False, f"La contraseña debe tener al menos {min_length} caracteres"
    
    # Verificar que tenga al menos una letra
    if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', password):
        return False, "La contraseña debe contener al menos una letra"
    
    # Verificar que tenga al menos un número
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    return True, ""


def get_placeholder_by_field(field_name: str) -> str:
    """
    Obtiene placeholder descriptivo para cada campo.
    
    Args:
        field_name: Nombre del campo
        
    Returns:
        Texto del placeholder
    """
    placeholders = {
        'nombre': 'Ej: Juan Carlos',
        'apellido': 'Ej: Pérez García',
        'nombre_usuario': 'Ej: juan.perez',
        'email': 'Ej: juan.perez@mctc.gob.ar',
        'contrasena': 'Mínimo 6 caracteres',
        'dni': 'Ej: 12345678',
        'cargo': 'Ej: Técnico Superior',
        'categoria': 'Ej: Planta Permanente',
        'marca': 'Ej: Toyota',
        'modelo': 'Ej: Corolla',
        'patente': 'Ej: ABC123',
        'consumo': 'Ej: 8.5'
    }
    
    return placeholders.get(field_name, f"Ingrese {field_name}")