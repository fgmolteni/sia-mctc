#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
"""
Script de prueba para crear un usuario y probar la funcionalidad de perfiles dinámicos.
"""

from components.db_users import create_user
from sia.models.validation import UserCreate

def create_test_user():
    """Crear un usuario de prueba para testing."""
    
    # Datos del usuario de prueba
    test_user = UserCreate(
        nombre="Juan Carlos",
        apellido="Pérez González", 
        nombre_usuario="jperez",
        email="juan.perez@mctc.gov.py",
        dni=12345678,
        contrasena="test123",
        rol="admin"
    )
    
    print("🔧 Creando usuario de prueba...")
    success, message, user_id = create_user(test_user)
    
    if success:
        print(f"✅ Usuario creado exitosamente con ID: {user_id}")
        print(f"📧 Email: {test_user.email}")
        print(f"👤 Usuario: {test_user.nombre_usuario}")
        print(f"🎭 Rol: {test_user.rol}")
        print(f"🆔 DNI: {test_user.dni}")
        return user_id
    else:
        print(f"❌ Error al crear usuario: {message}")
        return None

if __name__ == "__main__":
    user_id = create_test_user()
    if user_id:
        print(f"\n🌐 URL de prueba: http://localhost:8004/users/profile/{user_id}")
        print("💡 También puedes navegar desde la tabla de usuarios en http://localhost:8004/users")