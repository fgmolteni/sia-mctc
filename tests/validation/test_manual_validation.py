#!/usr/bin/env python3
"""Prueba manual simple de validaciones"""

# Importar las funciones directamente para probar
import re
from typing import Dict, Any

# Simular las funciones de validación
def get_user_validation_rules() -> Dict[str, Dict[str, Any]]:
    return {
        'nombre': {
            'min_length': 1,
            'max_length': 100,
            'pattern': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$',
            'pattern_name': 'nombre',
        },
        'email': {
            'min_length': 5,
            'max_length': 255,
            'email': True,
        },
        'dni': {
            'min_length': 7,
            'max_length': 8,
            'pattern': r'^\d{7,8}$',
            'optional': True,
            'custom_validation': 'dni_argentino'
        },
        'contrasena': {
            'password': True,
            'min_length': 6,
        }
    }

def validate_dni_argentino(dni: str) -> tuple[bool, str]:
    if not dni:
        return False, "El DNI no puede estar vacío"
    
    dni_clean = re.sub(r'[.\s-]', '', dni.strip())
    
    if not re.match(r'^\d{7,8}$', dni_clean):
        return False, "DNI debe tener 7-8 dígitos numéricos"
    
    dni_num = int(dni_clean)
    if dni_num < 1000000 or dni_num > 99999999:
        return False, "DNI fuera del rango válido"
    
    return True, ""

def _get_field_display_name(field_name: str) -> str:
    display_names = {
        'nombre': 'nombre',
        'email': 'email',
        'dni': 'DNI',
        'contrasena': 'contraseña'
    }
    return display_names.get(field_name, field_name)

def _get_pattern_error_message(field_name: str, rules: Dict[str, Any]) -> str:
    error_messages = {
        'nombre': 'El nombre debe contener solo letras y espacios'
    }
    return error_messages.get(field_name, f"Formato de {_get_field_display_name(field_name)} inválido")

def _validate_password(password: str, rules: Dict[str, Any]) -> tuple[bool, str]:
    min_length = rules.get('min_length', 6)
    
    if len(password) < min_length:
        return False, f"La contraseña debe tener al menos {min_length} caracteres"
    
    if not re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]', password):
        return False, "La contraseña debe contener al menos una letra"
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número"
    
    return True, ""

def validate_field_value(field_name: str, value: str, validation_rules: Dict[str, Dict[str, Any]] = None) -> tuple[bool, str]:
    if validation_rules is None:
        validation_rules = get_user_validation_rules()
    
    if field_name not in validation_rules:
        return True, ""
    
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
    
    # Validación de patrón regex
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
            if value_str:
                return validate_dni_argentino(value_str)
    
    return True, ""

# Ejecutar las pruebas
if __name__ == "__main__":
    print("🧪 PRUEBAS MANUALES DE VALIDACIÓN")
    print("=" * 40)
    
    rules = get_user_validation_rules()
    
    # Casos de prueba
    test_cases = [
        ('nombre', 'Juan', True),
        ('nombre', 'Juan123', False),
        ('nombre', '', False),
        ('email', 'juan@ejemplo.com', True),
        ('email', 'invalido', False),
        ('dni', '12345678', True),
        ('dni', '', True),  # Opcional
        ('dni', '123', False),
        ('contrasena', 'abc123', True),
        ('contrasena', '123456', False),
    ]
    
    passed = 0
    for campo, valor, esperado in test_cases:
        is_valid, error_msg = validate_field_value(campo, valor, rules)
        resultado = "✓" if is_valid == esperado else "✗"
        estado = "VÁLIDO" if is_valid else f"ERROR: {error_msg}"
        
        print(f"{resultado} {campo} '{valor}' -> {estado}")
        
        if is_valid == esperado:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(test_cases)} pruebas pasadas")
    print("✅ Función validada correctamente" if passed == len(test_cases) else "❌ Hay errores")