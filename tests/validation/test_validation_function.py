#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento de la función validate_field_value.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.abspath('.'))

from sia.components.forms.inputs._validation import (
    validate_field_value, 
    get_user_validation_rules
)

def test_validation_cases():
    """Prueba todos los casos de validación para cada campo."""
    
    print("🧪 INICIANDO PRUEBAS DE VALIDACIÓN")
    print("=" * 50)
    
    # Obtener las reglas de validación
    rules = get_user_validation_rules()
    
    # Casos de prueba para cada campo
    test_cases = {
        'nombre': {
            'valid': [
                'Juan', 'María José', 'José Luis', 'Ana María García',
                'Carlos Andrés', 'Sofía'
            ],
            'invalid': [
                '', '  ', 'Juan123', 'María@José', 'A' * 101, 'Juan-Carlos',
                'María_José', 'José.Luis'
            ]
        },
        'apellido': {
            'valid': [
                'Pérez', 'García López', 'Martínez', 'De la Torre',
                'Fernández García', 'López'
            ],
            'invalid': [
                '', '  ', 'Pérez123', 'García@López', 'A' * 101, 
                'Pérez-García', 'López_Martínez'
            ]
        },
        'nombre_usuario': {
            'valid': [
                'juan.perez', 'maria_garcia', 'carlos123', 'ana-lopez',
                'user123', 'test.user', 'admin_user'
            ],
            'invalid': [
                '', '  ', 'ju', 'usuario con espacios', 'user@domain',
                'A' * 51, 'user#123', 'user!', 'usuario_muy_largo_que_excede_limite'
            ]
        },
        'email': {
            'valid': [
                'juan@ejemplo.com', 'maria.garcia@mctc.gob.ar', 
                'test123@domain.org', 'user+tag@example.co.uk'
            ],
            'invalid': [
                '', '  ', 'abc', 'juan@', '@domain.com', 'user@domain',
                'user..double@domain.com', 'user @domain.com', 
                'A' * 250 + '@domain.com'
            ]
        },
        'dni': {
            'valid': [
                '', '  ', '12345678', '1234567', '45678901', '87654321'
            ],
            'invalid': [
                '123456', '123456789', 'abcdefgh', '12.345.678',
                '12 345 678', '999999', '99999999'
            ]
        },
        'contrasena': {
            'valid': [
                'abc123', 'password1', 'test123', 'secure1234',
                'MyPass1', 'contraseña123'
            ],
            'invalid': [
                '', '  ', '123', 'abcde', '12345', 'password', 
                '123456', 'ABCDEF'
            ]
        }
    }
    
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for field_name, cases in test_cases.items():
        print(f"\n📋 PROBANDO CAMPO: {field_name.upper()}")
        print("-" * 30)
        
        # Probar casos válidos
        print("✅ Casos válidos:")
        for value in cases['valid']:
            total_tests += 1
            is_valid, error_msg = validate_field_value(field_name, value, rules)
            display_value = f"'{value}'" if value.strip() else "vacío"
            
            if is_valid:
                passed_tests += 1
                print(f"  ✓ {display_value}: VÁLIDO")
            else:
                failed_tests.append(f"{field_name} - {display_value}: esperado VÁLIDO, obtuvo ERROR: {error_msg}")
                print(f"  ✗ {display_value}: ERROR - {error_msg}")
        
        # Probar casos inválidos
        print("❌ Casos inválidos:")
        for value in cases['invalid']:
            total_tests += 1
            is_valid, error_msg = validate_field_value(field_name, value, rules)
            display_value = f"'{value}'" if value.strip() else "vacío"
            
            if not is_valid:
                passed_tests += 1
                print(f"  ✓ {display_value}: ERROR - {error_msg}")
            else:
                failed_tests.append(f"{field_name} - {display_value}: esperado ERROR, obtuvo VÁLIDO")
                print(f"  ✗ {display_value}: VÁLIDO (esperaba error)")
    
    # Probar casos especiales
    print(f"\n🔍 CASOS ESPECIALES")
    print("-" * 30)
    
    # Valores None
    total_tests += 1
    is_valid, error_msg = validate_field_value('nombre', None, rules)
    if not is_valid:
        passed_tests += 1
        print(f"  ✓ None en nombre: ERROR - {error_msg}")
    else:
        failed_tests.append("nombre - None: esperado ERROR, obtuvo VÁLIDO")
        print(f"  ✗ None en nombre: VÁLIDO (esperaba error)")
    
    # Campo inexistente
    total_tests += 1
    is_valid, error_msg = validate_field_value('campo_inexistente', 'valor', rules)
    if is_valid and error_msg == "":
        passed_tests += 1
        print(f"  ✓ Campo inexistente: VÁLIDO (comportamiento esperado)")
    else:
        failed_tests.append("campo_inexistente: esperado VÁLIDO, obtuvo ERROR")
        print(f"  ✗ Campo inexistente: ERROR - {error_msg}")
    
    # DNI opcional vacío
    total_tests += 1
    is_valid, error_msg = validate_field_value('dni', '', rules)
    if is_valid:
        passed_tests += 1
        print(f"  ✓ DNI vacío (opcional): VÁLIDO")
    else:
        failed_tests.append("dni vacío: esperado VÁLIDO, obtuvo ERROR")
        print(f"  ✗ DNI vacío: ERROR - {error_msg}")
    
    # Resumen final
    print(f"\n📊 RESUMEN DE PRUEBAS")
    print("=" * 50)
    print(f"Total de pruebas: {total_tests}")
    print(f"Pruebas exitosas: {passed_tests}")
    print(f"Pruebas fallidas: {len(failed_tests)}")
    print(f"Porcentaje de éxito: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests:
        print(f"\n❌ PRUEBAS FALLIDAS:")
        for failure in failed_tests:
            print(f"  • {failure}")
        return False
    else:
        print(f"\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        return True

def test_specific_messages():
    """Prueba que los mensajes de error sean específicos y en español."""
    
    print(f"\n🗣️  PROBANDO MENSAJES DE ERROR ESPECÍFICOS")
    print("=" * 50)
    
    rules = get_user_validation_rules()
    
    # Casos específicos para probar mensajes
    test_messages = [
        ('nombre', 'Juan123', 'debe contener solo letras y espacios'),
        ('email', 'invalido', 'no tiene un formato válido'),
        ('contrasena', '12345', 'debe tener al menos 6 caracteres'),
        ('contrasena', 'abcdef', 'debe contener al menos un número'),
        ('contrasena', '123456', 'debe contener al menos una letra'),
        ('dni', '123', 'debe tener 7-8 dígitos numéricos'),
        ('nombre_usuario', 'ab', 'debe tener al menos 3 caracteres'),
    ]
    
    for field, value, expected_phrase in test_messages:
        is_valid, error_msg = validate_field_value(field, value, rules)
        if not is_valid and expected_phrase in error_msg.lower():
            print(f"  ✓ {field} '{value}': '{error_msg}'")
        else:
            print(f"  ✗ {field} '{value}': '{error_msg}' (esperaba: '{expected_phrase}')")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DE VALIDACIÓN DE CAMPOS")
    print("=" * 60)
    
    try:
        # Ejecutar las pruebas
        success = test_validation_cases()
        test_specific_messages()
        
        if success:
            print(f"\n✅ RESULTADO: La función validate_field_value está funcionando correctamente")
            sys.exit(0)
        else:
            print(f"\n❌ RESULTADO: Se encontraron problemas en la función validate_field_value")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 ERROR DURANTE LAS PRUEBAS: {e}")
        import traceback
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        traceback.print_exc()
        sys.exit(1)