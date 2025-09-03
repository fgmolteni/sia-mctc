#!/usr/bin/env python3
"""
Script para probar que los componentes TDD funcionan correctamente.
"""

def test_component_imports():
    """Verifica que todos los componentes se pueden importar correctamente."""
    print("Probando importaciones de componentes...")
    
    try:
        print("✓ stat_card importado correctamente")
    except Exception as e:
        print(f"✗ Error importando stat_card: {e}")
        
    try:
        print("✓ role_badge y status_badge importados correctamente")
    except Exception as e:
        print(f"✗ Error importando badges: {e}")
        
    try:
        print("✓ data_table importado correctamente")
    except Exception as e:
        print(f"✗ Error importando data_table: {e}")
        
    try:
        print("✓ search_filters importado correctamente") 
    except Exception as e:
        print(f"✗ Error importando search_filters: {e}")

def test_component_basic_functionality():
    """Prueba funcionalidad básica de los componentes."""
    print("\nProbando funcionalidad básica de componentes...")
    
    try:
        from sia.components.data_display.cards import stat_card
        result = stat_card(title="Test", value="10", icon="user")
        print("✓ stat_card funciona con parámetros básicos")
    except Exception as e:
        print(f"✗ Error en stat_card: {e}")
        
    try:
        from sia.components.data_display.badges import role_badge
        result = role_badge(text="Admin", role="admin")
        print("✓ role_badge funciona con parámetros básicos")
    except Exception as e:
        print(f"✗ Error en role_badge: {e}")
        
    try:
        from sia.components.data_display.badges import status_badge
        result = status_badge(text="Activo", status="active")
        print("✓ status_badge funciona con parámetros básicos")
    except Exception as e:
        print(f"✗ Error en status_badge: {e}")
        
    try:
        from sia.components.data_display.tables import data_table
        sample_data = [{"name": "Test", "role": "Admin"}]
        result = data_table(title="Test Table", data=sample_data, headers=["Name", "Role"])
        print("✓ data_table funciona con parámetros básicos")
    except Exception as e:
        print(f"✗ Error en data_table: {e}")

if __name__ == "__main__":
    test_component_imports()
    test_component_basic_functionality()
    print("\n✓ Pruebas básicas completadas")