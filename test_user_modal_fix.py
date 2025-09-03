#!/usr/bin/env python3
"""
Script de validación para probar las correcciones del sistema de usuarios.

Prueba:
1. Conexión a base de datos
2. Validación de modelos Pydantic 
3. Operaciones CRUD con campo email
4. Funciones de UserState
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.db_common import get_db_engine
from components.db_users import create_user, get_all_users, update_user, delete_user, get_user_by_id
from sia.models.validation import User, UserCreate, UserUpdate
from components.logging import get_sia_logger
from sqlalchemy import text
import uuid

logger = get_sia_logger('validation')

def test_database_connection():
    """Probar conexión a base de datos y estructura de tabla."""
    print("\n1. Probando conexión a base de datos...")
    
    engine = get_db_engine()
    if engine is None:
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        with engine.connect() as connection:
            # Verificar si la columna email existe
            query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'usuarios' AND column_name = 'email'
            """)
            result = connection.execute(query).fetchone()
            
            if result:
                print("✅ Conexión exitosa y columna email existe")
            else:
                print("❌ Error: Columna email no existe. Ejecute migrate_email.py primero")
                return False
                
    except Exception as e:
        print(f"❌ Error al verificar estructura: {e}")
        return False
    finally:
        engine.dispose()
        
    return True

def test_pydantic_models():
    """Probar validación de modelos Pydantic."""
    print("\n2. Probando validación de modelos Pydantic...")
    
    try:
        # Probar UserCreate con email válido
        user_data = UserCreate(
            nombre="Test",
            apellido="Usuario",
            nombre_usuario="test_user",
            email="test@ejemplo.com",
            contrasena="test123",
            rol="usuario"
        )
        print("✅ UserCreate con email válido")
        
        # Probar UserUpdate con email
        update_data = UserUpdate(
            nombre="Test Actualizado",
            email="nuevo@ejemplo.com"
        )
        print("✅ UserUpdate con email válido")
        
        # Probar validación de email inválido
        try:
            invalid_user = UserCreate(
                nombre="Test",
                apellido="Usuario", 
                nombre_usuario="test",
                email="email_invalido",  # Sin @
                contrasena="test123",
                rol="usuario"
            )
            print("❌ Error: Debería haber fallado con email inválido")
            return False
        except:
            print("✅ Validación de email inválido funciona correctamente")
            
    except Exception as e:
        print(f"❌ Error en validación Pydantic: {e}")
        return False
        
    return True

def test_crud_operations():
    """Probar operaciones CRUD con campo email."""
    print("\n3. Probando operaciones CRUD...")
    
    # Generar email único para prueba
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"test_{unique_id}@ejemplo.com"
    test_username = f"test_user_{unique_id}"
    
    try:
        # Crear usuario
        print("   Probando CREATE...")
        user_data = UserCreate(
            nombre="Test",
            apellido="CRUD",
            nombre_usuario=test_username,
            email=test_email,
            contrasena="test123",
            rol="usuario"
        )
        
        success, message, user_id = create_user(user_data)
        if not success:
            print(f"❌ Error creando usuario: {message}")
            return False
        print(f"✅ Usuario creado con ID: {user_id}")
        
        # Leer usuario
        print("   Probando READ...")
        success, message, users = get_all_users()
        if not success:
            print(f"❌ Error leyendo usuarios: {message}")
            return False
        
        # Buscar nuestro usuario
        test_user = None
        for user in users:
            if user.email == test_email:
                test_user = user
                break
                
        if not test_user:
            print("❌ Error: Usuario creado no encontrado en lista")
            return False
        print(f"✅ Usuario encontrado: {test_user.email}")
        
        # Actualizar usuario
        print("   Probando UPDATE...")
        new_email = f"updated_{unique_id}@ejemplo.com"
        update_data = UserUpdate(
            nombre="Test Actualizado",
            email=new_email
        )
        
        success, message, updated_user = update_user(user_id, update_data)
        if not success:
            print(f"❌ Error actualizando usuario: {message}")
            return False
        print(f"✅ Usuario actualizado: {updated_user.email}")
        
        # Verificar actualización
        success, message, user_by_id = get_user_by_id(user_id)
        if not success or user_by_id.email != new_email:
            print("❌ Error: Actualización no se persistió correctamente")
            return False
        print("✅ Actualización verificada")
        
        # Limpiar - eliminar usuario de prueba
        print("   Limpiando...")
        from components.db_users import delete_user
        success, message = delete_user(user_id)
        if success:
            print("✅ Usuario de prueba eliminado")
        else:
            print(f"⚠️ No se pudo eliminar usuario de prueba: {message}")
            
    except Exception as e:
        print(f"❌ Error en operaciones CRUD: {e}")
        return False
        
    return True

def test_duplicate_validation():
    """Probar validación de duplicados."""
    print("\n4. Probando validación de duplicados...")
    
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"dup_test_{unique_id}@ejemplo.com"
    test_username = f"dup_user_{unique_id}"
    
    try:
        # Crear primer usuario
        user_data1 = UserCreate(
            nombre="Dup",
            apellido="Test1",
            nombre_usuario=test_username,
            email=test_email,
            contrasena="test123",
            rol="usuario"
        )
        
        success, message, user_id1 = create_user(user_data1)
        if not success:
            print(f"❌ Error creando primer usuario: {message}")
            return False
            
        # Intentar crear usuario con mismo email
        user_data2 = UserCreate(
            nombre="Dup",
            apellido="Test2", 
            nombre_usuario=f"otro_{test_username}",
            email=test_email,  # Email duplicado
            contrasena="test123",
            rol="usuario"
        )
        
        success, message, user_id2 = create_user(user_data2)
        if success:
            print("❌ Error: Debería haber fallado con email duplicado")
            # Limpiar usuarios creados
            delete_user(user_id1)
            delete_user(user_id2)
            return False
            
        print("✅ Validación de email duplicado funciona correctamente")
        
        # Limpiar
        delete_user(user_id1)
        
    except Exception as e:
        print(f"❌ Error en prueba de duplicados: {e}")
        return False
        
    return True

def main():
    """Ejecutar todas las pruebas."""
    print("=== VALIDACIÓN DE CORRECCIONES DEL SISTEMA DE USUARIOS ===")
    
    tests = [
        ("Conexión a Base de Datos", test_database_connection),
        ("Modelos Pydantic", test_pydantic_models), 
        ("Operaciones CRUD", test_crud_operations),
        ("Validación de Duplicados", test_duplicate_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Excepción en {test_name}: {e}")
    
    print(f"\n=== RESULTADOS ===")
    print(f"Pruebas pasadas: {passed}/{total}")
    
    if passed == total:
        print("✅ Todas las pruebas pasaron. El sistema está listo para usar.")
        return 0
    else:
        print("❌ Algunas pruebas fallaron. Revisar los errores anteriores.")
        return 1

if __name__ == "__main__":
    sys.exit(main())