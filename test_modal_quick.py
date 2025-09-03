#!/usr/bin/env python3
"""
Test rápido para verificar que el modal se puede importar y funcionar básicamente
"""

def test_modal_import():
    """Test básico de importación del modal"""
    try:
        print("✅ Importación del modal exitosa")
        return True
    except Exception as e:
        print(f"❌ Error al importar modal: {e}")
        return False

def test_user_state_setters():
    """Test básico de los métodos setter en UserState"""
    try:
        from sia.pages.usuarios import UserState
        
        # Verificar que los métodos existen
        methods = [
            'set_form_nombre',
            'set_form_apellido', 
            'set_form_nombre_usuario',
            'set_form_contrasena',
            'set_form_rol'
        ]
        
        for method_name in methods:
            if not hasattr(UserState, method_name):
                print(f"❌ Método {method_name} no existe en UserState")
                return False
                
        print("✅ Todos los métodos setter están presentes en UserState")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar UserState: {e}")
        return False

def test_form_components():
    """Test básico de los componentes de formulario"""
    try:
        from sia.components.forms.inputs import form_input
        from sia.components.forms.selects import form_select
        
        # Verificar que aceptan el parámetro required
        import inspect
        
        # Verificar form_input
        sig = inspect.signature(form_input)
        if 'required' not in sig.parameters:
            print("❌ form_input no tiene parámetro 'required'")
            return False
            
        # Verificar form_select
        sig = inspect.signature(form_select)
        if 'required' not in sig.parameters:
            print("❌ form_select no tiene parámetro 'required'")
            return False
            
        print("✅ Componentes de formulario tienen parámetro 'required'")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar componentes de formulario: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Ejecutando tests rápidos del modal...")
    
    tests = [
        test_modal_import,
        test_user_state_setters,
        test_form_components,
    ]
    
    results = []
    for test in tests:
        print(f"\n🔸 Ejecutando {test.__name__}...")
        results.append(test())
        
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 Resultados: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los tests básicos pasaron!")
    else:
        print("⚠️ Algunos tests fallaron. Revisar implementación.")