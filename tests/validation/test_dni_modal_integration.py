#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
"""
Test básico de integración del modal de usuario con campo DNI.
Verifica que no hay errores de importación o sintaxis.
"""

def test_modal_import():
    """Prueba que el modal se pueda importar sin errores."""
    try:
        from sia.components.forms.modals._user_modal import user_modal
        print("✅ Modal de usuario importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando modal de usuario: {e}")
        return False

def test_userstate_import():
    """Prueba que el UserState se pueda importar sin errores."""
    try:
        from sia.pages.usuarios import UserState
        print("✅ UserState importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando UserState: {e}")
        return False

def test_validation_import():
    """Prueba que las validaciones se puedan importar sin errores."""
    try:
        from sia.components.forms.inputs._validation import (
            get_user_validation_rules,
            validate_dni_argentino
        )
        print("✅ Validaciones importadas correctamente")
        return True
    except Exception as e:
        print(f"❌ Error importando validaciones: {e}")
        return False

def test_validation_rules():
    """Prueba que las reglas de validación del DNI estén correctas."""
    try:
        from sia.components.forms.inputs._validation import get_user_validation_rules
        
        rules = get_user_validation_rules()
        dni_rules = rules.get('dni', {})
        
        # Verificar que las reglas del DNI estén correctas
        assert 'min_length' in dni_rules, "Falta min_length en reglas DNI"
        assert 'max_length' in dni_rules, "Falta max_length en reglas DNI"
        assert 'pattern' in dni_rules, "Falta pattern en reglas DNI"
        assert 'helper_text' in dni_rules, "Falta helper_text en reglas DNI"
        assert dni_rules['min_length'] == 7, "min_length del DNI debe ser 7"
        assert dni_rules['max_length'] == 8, "max_length del DNI debe ser 8"
        assert dni_rules['pattern'] == r'^\d{7,8}$', "Pattern del DNI incorrecto"
        
        print("✅ Reglas de validación del DNI correctas")
        return True
    except Exception as e:
        print(f"❌ Error verificando reglas de validación: {e}")
        return False

def test_dni_validation():
    """Prueba la función de validación de DNI."""
    try:
        from sia.components.forms.inputs._validation import validate_dni_argentino
        
        # Casos de prueba
        test_cases = [
            ("12345678", True, "DNI válido de 8 dígitos"),
            ("1234567", True, "DNI válido de 7 dígitos"),
            ("123456", False, "DNI muy corto"),
            ("123456789", False, "DNI muy largo"),
            ("12345abc", False, "DNI con letras"),
            ("", False, "DNI vacío")
        ]
        
        for dni, expected, desc in test_cases:
            is_valid, _ = validate_dni_argentino(dni)
            assert is_valid == expected, f"Fallo en {desc}: {dni}"
        
        print("✅ Función de validación de DNI funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error probando validación de DNI: {e}")
        return False

def test_userstate_dni_field():
    """Prueba que el UserState tenga el campo DNI y sus métodos."""
    try:
        from sia.pages.usuarios import UserState
        
        # Crear instancia del estado
        state = UserState()
        
        # Verificar que tiene los campos necesarios
        assert hasattr(state, 'form_dni'), "UserState debe tener form_dni"
        assert hasattr(state, 'set_form_dni'), "UserState debe tener set_form_dni"
        
        # Probar el setter de DNI
        state.set_form_dni("12.345.678")
        assert state.form_dni == "12345678", "set_form_dni debe limpiar caracteres no numéricos"
        
        state.set_form_dni("1234567")
        assert state.form_dni == "1234567", "set_form_dni debe mantener números válidos"
        
        print("✅ UserState maneja correctamente el campo DNI")
        return True
    except Exception as e:
        print(f"❌ Error probando UserState DNI: {e}")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("🔍 Verificando integración del campo DNI en el modal de usuario...\n")
    
    tests = [
        test_modal_import,
        test_userstate_import,
        test_validation_import,
        test_validation_rules,
        test_dni_validation,
        test_userstate_dni_field
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error ejecutando {test.__name__}: {e}")
            failed += 1
        print()
    
    print(f"📊 Resumen: {passed} pruebas pasaron, {failed} fallaron")
    
    if failed == 0:
        print("🎉 ¡Todas las pruebas pasaron! El campo DNI está correctamente integrado.")
        return True
    else:
        print("⚠️  Hay errores que necesitan corrección.")
        return False

if __name__ == "__main__":
    main()