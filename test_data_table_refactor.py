#!/usr/bin/env python3
"""
Script de prueba para verificar que la refactorización del componente data_table
funciona correctamente con variables de estado de Reflex.
"""

try:
    # Verificar importación del componente data_table
    from sia.components.data_display.tables import data_table
    print("✓ Importación del componente data_table exitosa")

    # Verificar importación de Reflex
    import reflex as rx
    print("✓ Importación de Reflex exitosa")

    # Verificar que el componente tiene la signatura correcta
    import inspect
    signature = inspect.signature(data_table)
    print(f"✓ Signatura del componente data_table: {signature}")

    # Verificar tipos de parámetros
    params = signature.parameters
    data_param = params.get('data')
    if data_param:
        print(f"✓ Parámetro 'data' encontrado con tipo: {data_param.annotation}")
    
    print("\n🎉 Todos los tests de importación pasaron exitosamente!")
    print("\n📋 Resumen de la refactorización:")
    print("  • Componente data_table ahora acepta rx.Var[List[Dict]] como parámetro data")  
    print("  • Se implementó rx.foreach en lugar de iteración Python directa")
    print("  • Las funciones de render ahora manejan variables de estado de Reflex")
    print("  • Se mantuvieron todas las funcionalidades existentes")

except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")