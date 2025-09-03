#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que las importaciones de componentes funcionan correctamente.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_form_inputs_imports():
    """Verifica importaciones de form inputs"""
    try:
        print("🔄 Probando importaciones de form inputs...")
        
        from sia.components.forms.inputs import (
            form_input, 
            form_date_input, 
            form_time_input,
            password_input_with_strength,
            select_input
        )
        
        print("✅ form_input - OK")
        print("✅ form_date_input - OK") 
        print("✅ form_time_input - OK")
        print("✅ password_input_with_strength - OK")
        print("✅ select_input - OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_gallery_imports():
    """Verifica importaciones de la galería"""
    try:
        print("\n🔄 Probando importaciones de gallery.py...")
        
        from sia.pages.gallery import gallery_page
        print("✅ gallery_page - OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación en gallery: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado en gallery: {e}")
        return False

def test_forms_views_imports():
    """Verifica importaciones de forms_views"""
    try:
        print("\n🔄 Probando importaciones de forms_views.py...")
        
        from sia.views.forms_views import FormState, forms_views
        print("✅ FormState - OK")
        print("✅ forms_views - OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación en forms_views: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado en forms_views: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🧪 Iniciando verificación de importaciones corregidas...\n")
    
    tests = [
        test_form_inputs_imports,
        test_gallery_imports,
        test_forms_views_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Resultados: {passed}/{total} pruebas de importación pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las importaciones funcionan correctamente!")
        return True
    else:
        print("⚠️  Algunas importaciones fallan. Revise los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)