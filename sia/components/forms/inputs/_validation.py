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