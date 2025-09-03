#!/usr/bin/env python3
"""
Script de prueba para diagnosticar problemas con las estadísticas de usuarios.
"""

import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from components.db_users import get_user_statistics, get_all_users
from components.db_common import get_db_engine
from sqlalchemy import text

def test_database_connection():
    """Prueba la conexión a la base de datos."""
    print("=== PRUEBA DE CONEXIÓN A BASE DE DATOS ===")
    
    engine = get_db_engine()
    if engine is None:
        print("❌ Error: No se pudo obtener la conexión a la base de datos")
        return False
    
    try:
        with engine.connect() as connection:
            # Probar una query simple
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()
            print(f"✅ Conexión exitosa. PostgreSQL versión: {version[0]}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    finally:
        engine.dispose()

def test_users_table():
    """Prueba que la tabla de usuarios existe y tiene datos."""
    print("\n=== PRUEBA DE TABLA USUARIOS ===")
    
    engine = get_db_engine()
    if engine is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        with engine.connect() as connection:
            # Verificar si la tabla existe
            check_table = text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'usuarios'
                )
            """)
            table_exists = connection.execute(check_table).scalar()
            
            if not table_exists:
                print("❌ Error: La tabla 'usuarios' no existe")
                return False
            
            print("✅ La tabla 'usuarios' existe")
            
            # Contar usuarios totales
            count_query = text("SELECT COUNT(*) FROM usuarios")
            total_count = connection.execute(count_query).scalar()
            print(f"✅ Total de usuarios en la tabla: {total_count}")
            
            if total_count == 0:
                print("⚠️ Advertencia: No hay usuarios en la tabla")
                return False
                
            # Mostrar algunos usuarios de ejemplo
            sample_query = text("""
                SELECT id, nombre, apellido, nombre_usuario, rol 
                FROM usuarios 
                LIMIT 5
            """)
            sample_users = connection.execute(sample_query).fetchall()
            
            print("\n📋 Usuarios de ejemplo:")
            for user in sample_users:
                print(f"  ID: {user[0]}, Nombre: {user[1]} {user[2]}, Usuario: {user[3]}, Rol: {user[4]}")
                
            return True
            
    except Exception as e:
        print(f"❌ Error al verificar tabla usuarios: {e}")
        return False
    finally:
        engine.dispose()

def test_statistics_query():
    """Prueba la query de estadísticas directamente."""
    print("\n=== PRUEBA DE QUERY DE ESTADÍSTICAS ===")
    
    engine = get_db_engine()
    if engine is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        with engine.connect() as connection:
            # Ejecutar la misma query que usa get_user_statistics()
            query = text("""
                SELECT 
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN rol = 'admin' THEN 1 END) as admin_count,
                    COUNT(CASE WHEN rol = 'supervisor' THEN 1 END) as supervisor_count,
                    COUNT(CASE WHEN rol = 'usuario' THEN 1 END) as user_count
                FROM usuarios
            """)
            
            result = connection.execute(query).fetchone()
            
            print("📊 Resultados de la query de estadísticas:")
            print(f"  Total usuarios: {result[0]}")
            print(f"  Administradores: {result[1]}")
            print(f"  Supervisores: {result[2]}")
            print(f"  Usuarios comunes: {result[3]}")
            
            # Verificar distribución por roles
            roles_query = text("SELECT rol, COUNT(*) FROM usuarios GROUP BY rol")
            roles_result = connection.execute(roles_query).fetchall()
            
            print("\n👥 Distribución por roles:")
            for role, count in roles_result:
                print(f"  {role}: {count}")
                
            return True
            
    except Exception as e:
        print(f"❌ Error al ejecutar query de estadísticas: {e}")
        return False
    finally:
        engine.dispose()

def test_get_user_statistics_function():
    """Prueba la función get_user_statistics()."""
    print("\n=== PRUEBA DE FUNCIÓN get_user_statistics() ===")
    
    try:
        success, message, stats = get_user_statistics()
        
        print(f"🔍 Resultado de la función:")
        print(f"  Success: {success}")
        print(f"  Message: {message}")
        print(f"  Stats: {stats}")
        
        if success:
            print("✅ La función get_user_statistics() funciona correctamente")
            return True
        else:
            print(f"❌ La función falló: {message}")
            return False
            
    except Exception as e:
        print(f"❌ Error al ejecutar get_user_statistics(): {e}")
        return False

def test_get_all_users_function():
    """Prueba la función get_all_users()."""
    print("\n=== PRUEBA DE FUNCIÓN get_all_users() ===")
    
    try:
        success, message, users = get_all_users()
        
        print(f"🔍 Resultado de la función:")
        print(f"  Success: {success}")
        print(f"  Message: {message}")
        print(f"  Usuarios encontrados: {len(users) if users else 0}")
        
        if success and users:
            print("✅ La función get_all_users() funciona correctamente")
            print("\n👤 Primeros 3 usuarios:")
            for i, user in enumerate(users[:3]):
                print(f"  {i+1}. {user.nombre} {user.apellido} ({user.rol})")
            return True
        else:
            print(f"❌ La función falló: {message}")
            return False
            
    except Exception as e:
        print(f"❌ Error al ejecutar get_all_users(): {e}")
        return False

def main():
    """Función principal de diagnóstico."""
    print("🔧 DIAGNÓSTICO DE ESTADÍSTICAS DE USUARIOS")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    tests = [
        test_database_connection,
        test_users_table,
        test_statistics_query,
        test_get_user_statistics_function,
        test_get_all_users_function
    ]
    
    passed_tests = 0
    
    for test in tests:
        try:
            if test():
                passed_tests += 1
        except Exception as e:
            print(f"❌ Error inesperado en {test.__name__}: {e}")
    
    print(f"\n📈 RESUMEN: {passed_tests}/{len(tests)} pruebas pasaron")
    
    if passed_tests == len(tests):
        print("✅ Todas las pruebas pasaron. El problema puede estar en la interfaz de usuario.")
    else:
        print("❌ Algunas pruebas fallaron. Revisar la configuración de la base de datos.")

if __name__ == "__main__":
    main()