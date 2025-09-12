#!/usr/bin/env python3
"""
Script definitivo para configurar usuario administrador SIA-MCTC.

Este script maneja todo el proceso de preparación y creación del usuario administrador:
1. Verifica conexión a PostgreSQL
2. Aplica migraciones necesarias (email y dni)
3. Crea usuario administrador con credenciales seguras
4. Verifica la creación exitosa

Credenciales del usuario administrador:
- Username: adm
- Password: adm1234  
- Email: admin@sia-mctc.local
- DNI: 12345678
- Rol: admin

Uso: python setup_admin_user.py
"""

import sys
import os

# Configurar path para importaciones
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

def main():
    print("🚀 SETUP USUARIO ADMINISTRADOR - SIA-MCTC")
    print("=" * 50)
    
    try:
        # Importar después de configurar path
        from components.db_common import get_db_engine
        from components.db_users import create_user
        from sia.models.validation import UserCreate
        from sqlalchemy import text
        
        # 1. Verificar conexión a base de datos
        print("1️⃣ Verificando conexión a PostgreSQL...")
        engine = get_db_engine()
        
        if engine is None:
            print("❌ ERROR: No se puede conectar a PostgreSQL")
            print("💡 Solución: Ejecuta 'docker compose up -d' para iniciar la base de datos")
            return False
        
        print("✅ Conexión a PostgreSQL exitosa")
        
        # 2. Verificar y aplicar migraciones de esquema
        print("\n2️⃣ Verificando estructura de base de datos...")
        
        try:
            with engine.connect() as connection:
                # Obtener columnas actuales
                result = connection.execute(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'usuarios' AND table_schema = current_schema()
                """))
                current_columns = [row[0] for row in result]
                
                print(f"📋 Columnas actuales: {', '.join(current_columns)}")
                
                # Verificar si necesita migración email
                needs_email = 'email' not in current_columns
                needs_dni = 'dni' not in current_columns
                
                if needs_email:
                    print("📦 Aplicando migración: campo email...")
                    try:
                        with connection.begin():
                            connection.execute(text("ALTER TABLE usuarios ADD COLUMN email VARCHAR(255)"))
                            connection.execute(text("UPDATE usuarios SET email = CONCAT(nombre_usuario, '@temp.local') WHERE email IS NULL"))
                            connection.execute(text("ALTER TABLE usuarios ALTER COLUMN email SET NOT NULL"))
                            connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email)"))
                        print("✅ Campo email agregado exitosamente")
                    except Exception as e:
                        print(f"❌ Error agregando campo email: {e}")
                        return False
                else:
                    print("✅ Campo email ya existe")
                
                if needs_dni:
                    print("📦 Aplicando migración: campo dni...")
                    try:
                        with connection.begin():
                            connection.execute(text("ALTER TABLE usuarios ADD COLUMN dni INTEGER"))
                            connection.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_dni ON usuarios(dni) WHERE dni IS NOT NULL"))
                        print("✅ Campo dni agregado exitosamente")
                    except Exception as e:
                        print(f"❌ Error agregando campo dni: {e}")
                        return False
                else:
                    print("✅ Campo dni ya existe")
                    
        except Exception as e:
            print(f"❌ Error verificando/actualizando esquema: {e}")
            return False
        finally:
            engine.dispose()
        
        # 3. Verificar si ya existe usuario admin
        print("\n3️⃣ Verificando usuarios existentes...")
        engine = get_db_engine()
        
        try:
            with engine.connect() as connection:
                # Buscar usuario admin existente
                admin_check = connection.execute(text("""
                    SELECT id, nombre, apellido, nombre_usuario, email, rol 
                    FROM usuarios 
                    WHERE nombre_usuario = 'adm' OR rol = 'admin'
                    LIMIT 1
                """)).fetchone()
                
                if admin_check:
                    print("⚠️  Ya existe un usuario administrador:")
                    print(f"   ID: {admin_check[0]}")
                    print(f"   Nombre: {admin_check[1]} {admin_check[2]}")
                    print(f"   Username: {admin_check[3]}")
                    print(f"   Email: {admin_check[4]}")
                    print(f"   Rol: {admin_check[5]}")
                    
                    respuesta = input("\n¿Deseas continuar creando otro usuario admin? (s/N): ").lower()
                    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
                        print("🛑 Proceso cancelado por el usuario")
                        return True
                        
        except Exception as e:
            print(f"❌ Error verificando usuarios existentes: {e}")
            return False
        finally:
            engine.dispose()
        
        # 4. Crear usuario administrador
        print("\n4️⃣ Creando usuario administrador...")
        
        try:
            # Datos del usuario administrador
            admin_data = UserCreate(
                nombre="Administrador",
                apellido="Sistema",
                nombre_usuario="adm",
                email="admin@sia-mctc.local",
                contrasena="adm1234",
                dni=12345678,
                rol="admin"
            )
            
            # Crear usuario usando función existente
            success, message, user_id = create_user(admin_data)
            
            if success:
                print("✅ Usuario administrador creado exitosamente!")
                print(f"   ID del usuario: {user_id}")
                print(f"   Mensaje: {message}")
            else:
                print(f"❌ Error creando usuario administrador: {message}")
                return False
                
        except Exception as e:
            print(f"❌ Error inesperado creando usuario: {e}")
            return False
        
        # 5. Verificación final
        print("\n5️⃣ Verificación final...")
        engine = get_db_engine()
        
        try:
            with engine.connect() as connection:
                verification = connection.execute(text("""
                    SELECT id, nombre, apellido, nombre_usuario, email, dni, rol, fecha_creacion
                    FROM usuarios 
                    WHERE nombre_usuario = 'adm'
                """)).fetchone()
                
                if verification:
                    print("✅ Verificación exitosa del usuario administrador:")
                    print(f"   ID: {verification[0]}")
                    print(f"   Nombre completo: {verification[1]} {verification[2]}")
                    print(f"   Username: {verification[3]}")
                    print(f"   Email: {verification[4]}")
                    print(f"   DNI: {verification[5]}")
                    print(f"   Rol: {verification[6]}")
                    print(f"   Fecha de creación: {verification[7]}")
                else:
                    print("❌ Error: No se pudo verificar el usuario creado")
                    return False
                    
        except Exception as e:
            print(f"❌ Error en verificación final: {e}")
            return False
        finally:
            engine.dispose()
        
        # 6. Resumen final
        print("\n" + "=" * 50)
        print("🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print("=" * 50)
        print("\n📋 CREDENCIALES DE ACCESO:")
        print("   🌐 URL: http://localhost:3000")
        print("   👤 Username: adm")
        print("   🔐 Password: adm1234")
        print("   📧 Email: admin@sia-mctc.local")
        print("   🆔 DNI: 12345678")
        print("   👑 Rol: Administrador")
        print("\n🔒 IMPORTANTE:")
        print("   - Cambia la contraseña después del primer acceso")
        print("   - Guarda estas credenciales de forma segura")
        print("   - El usuario tiene permisos completos del sistema")
        print("\n✨ El sistema SIA-MCTC está listo para usar!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de estar en el directorio correcto del proyecto")
        return False
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = main()
        exit_code = 0 if success else 1
        
        if not success:
            print("\n❌ El proceso falló. Revisa los errores anteriores.")
            print("\n🔧 Pasos para solucionar problemas:")
            print("   1. Verifica que PostgreSQL esté corriendo: docker compose up -d")
            print("   2. Verifica las variables de entorno en .env")
            print("   3. Ejecuta el script desde el directorio raíz del proyecto")
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Proceso interrumpido por el usuario")
        sys.exit(1)