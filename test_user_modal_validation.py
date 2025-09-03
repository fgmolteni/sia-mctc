#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que el modal de usuario mejorado funciona correctamente.
Este script verifica:
1. Importaciones correctas
2. Reglas de validación
3. Transformaciones automáticas  
4. Componentes de entrada mejorados
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Verifica que todas las importaciones funcionen correctamente."""
    try:
        print("🔄 Verificando importaciones...")
        
        # Test importación de validaciones
        from sia.components.forms.inputs import (
            get_user_validation_rules,
            get_placeholder_by_field,
            apply_auto_transform,
            form_input,
            password_input_with_strength
        )
        print("✅ Importaciones de validación - OK")
        
        # Test importación del modal
        from sia.components.forms.modals import user_modal
        print("✅ Importación del modal - OK")
        
        # Test importación del estado de usuarios
        from sia.pages.usuarios import UserState
        print("✅ Importación del estado - OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def test_validation_rules():
    """Verifica que las reglas de validación estén correctamente definidas."""
    try:
        print("\n🔄 Verificando reglas de validación...")
        
        from sia.components.forms.inputs import get_user_validation_rules
        
        rules = get_user_validation_rules()
        expected_fields = ['nombre', 'apellido', 'nombre_usuario', 'email', 'contrasena']
        
        for field in expected_fields:
            if field not in rules:
                print(f"❌ Campo faltante en reglas: {field}")
                return False
            
            print(f"✅ Reglas para {field}: {rules[field]}")
        
        print("✅ Reglas de validación - OK")
        return True
        
    except Exception as e:
        print(f"❌ Error en reglas de validación: {e}")
        return False


def test_placeholders():
    """Verifica que los placeholders estén definidos."""
    try:
        print("\n🔄 Verificando placeholders...")
        
        from sia.components.forms.inputs import get_placeholder_by_field
        
        fields = ['nombre', 'apellido', 'nombre_usuario', 'email', 'contrasena']
        
        for field in fields:
            placeholder = get_placeholder_by_field(field)
            print(f"✅ Placeholder para {field}: '{placeholder}'")
        
        print("✅ Placeholders - OK")
        return True
        
    except Exception as e:
        print(f"❌ Error en placeholders: {e}")
        return False


def test_transformations():
    """Verifica que las transformaciones automáticas funcionen."""
    try:
        print("\n🔄 Verificando transformaciones...")
        
        from sia.components.forms.inputs import apply_auto_transform
        
        # Test capitalización
        result = apply_auto_transform("juan carlos", "title")
        expected = "Juan Carlos"
        if result != expected:
            print(f"❌ Capitalización falló: esperado '{expected}', obtuvo '{result}'")
            return False
        print(f"✅ Capitalización: 'juan carlos' -> '{result}'")
        
        # Test minúsculas
        result = apply_auto_transform("JUAN.PEREZ", "lowercase")
        expected = "juan.perez"
        if result != expected:
            print(f"❌ Minúsculas falló: esperado '{expected}', obtuvo '{result}'")
            return False
        print(f"✅ Minúsculas: 'JUAN.PEREZ' -> '{result}'")
        
        # Test mayúsculas
        result = apply_auto_transform("abc123", "uppercase")
        expected = "ABC123"
        if result != expected:
            print(f"❌ Mayúsculas falló: esperado '{expected}', obtuvo '{result}'")
            return False
        print(f"✅ Mayúsculas: 'abc123' -> '{result}'")
        
        print("✅ Transformaciones automáticas - OK")
        return True
        
    except Exception as e:
        print(f"❌ Error en transformaciones: {e}")
        return False


def test_password_strength():
    """Verifica que la evaluación de fortaleza de contraseña funcione."""
    try:
        print("\n🔄 Verificando evaluación de fortaleza de contraseña...")
        
        from sia.components.forms.inputs._text import _evaluate_password_strength, get_strength_text, get_strength_color
        
        # Contraseña muy débil
        level = _evaluate_password_strength("123")
        text = get_strength_text(level)
        color = get_strength_color(level)
        print(f"✅ '123' -> Nivel: {level}, Texto: '{text}', Color: '{color}'")
        
        # Contraseña fuerte
        level = _evaluate_password_strength("MiPassword123!")
        text = get_strength_text(level)
        color = get_strength_color(level)
        print(f"✅ 'MiPassword123!' -> Nivel: {level}, Texto: '{text}', Color: '{color}'")
        
        print("✅ Evaluación de fortaleza - OK")
        return True
        
    except Exception as e:
        print(f"❌ Error en evaluación de fortaleza: {e}")
        return False


def main():
    """Función principal de prueba."""
    print("🧪 Iniciando pruebas del modal de usuario mejorado...\n")
    
    tests = [
        test_imports,
        test_validation_rules,
        test_placeholders,
        test_transformations,
        test_password_strength
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El modal de usuario mejorado está listo.")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revise los errores arriba.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)