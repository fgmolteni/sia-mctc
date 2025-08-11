from components.db_common import get_db_engine
from sqlalchemy import text
import bcrypt

def add_user(nombre: str, apellido: str, nombre_usuario: str, contrasena: str, rol: str = 'usuario') -> int | None:
    """
    Añade un nuevo usuario a la tabla 'usuarios' con la contraseña hasheada.
    Returns:
        int: El ID del usuario insertado, o None en caso de error.
    """
    engine = get_db_engine()
    if engine is None:
        return None

    hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        with engine.connect() as connection:
            with connection.begin():
                query = text("""
                    INSERT INTO usuarios (nombre, apellido, nombre_usuario, hash_contrasena, rol)
                    VALUES (:nombre, :apellido, :nombre_usuario, :hash_contrasena, :rol) RETURNING id;
                """)
                result = connection.execute(query, {
                    "nombre": nombre,
                    "apellido": apellido,
                    "nombre_usuario": nombre_usuario,
                    "hash_contrasena": hashed_password,
                    "rol": rol
                }).scalar_one()
            print(f"Usuario {nombre_usuario} añadido exitosamente con ID: {result}")
            return result
    except Exception as error:
        print(f"Error al añadir usuario: {error}")
        return None
    finally:
        if engine:
            engine.dispose()

def get_all_users():
    engine = get_db_engine()
    if engine is None:
        return []

    try:
        with engine.connect() as connection:
            query = text("SELECT nombre, apellido, nombre_usuario, rol FROM usuarios;")
            result = connection.execute(query).fetchall()
            users = [{'name': f'{row[0]} {row[1]}', 'email': row[2], 'role': row[3], 'area': 'Default', 'status': 'Activo', 'permissions': 0, 'attributes': 0, 'last_access': '', 'avatar': row[2][0].upper(), 'actions': ''} for row in result]
            return users
    except Exception as error:
        print(f"Error al obtener usuarios: {error}")
        return []
    finally:
        if engine:
            engine.dispose()


def verify_user(nombre_usuario: str, contrasena: str) -> int | None:
    """
    Verifica las credenciales de un usuario.
    Returns:
        int: El ID del usuario si las credenciales son válidas, o None en caso contrario.
    """
    engine = get_db_engine()
    if engine is None:
        return None

    try:
        with engine.connect() as connection:
            query = text("SELECT id, hash_contrasena FROM usuarios WHERE nombre_usuario = :nombre_usuario;")
            result = connection.execute(query, {"nombre_usuario": nombre_usuario}).fetchone()

            if result:
                user_id, stored_hash = result
                if bcrypt.checkpw(contrasena.encode('utf-8'), stored_hash.encode('utf-8')):
                    print(f"Usuario {nombre_usuario} autenticado exitosamente.")
                    return user_id
            print(f"Fallo de autenticación para el usuario {nombre_usuario}.")
            return None
    except Exception as error:
        print(f"Error al verificar usuario: {error}")
        return None
    finally:
        if engine:
            engine.dispose()
