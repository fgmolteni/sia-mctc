from components.db_common import get_db_engine
from sqlalchemy import text
import bcrypt
from components.logging import get_sia_logger, log_security_event
from sia.models.validation import User, UserCreate, UserUpdate
from typing import List, Optional
from pydantic import ValidationError

# Logger para este módulo
logger = get_sia_logger('database')

def create_user(user_data: UserCreate) -> tuple[bool, str, Optional[int]]:
    """
    Crea un nuevo usuario usando validación Pydantic.
    
    Args:
        user_data: Datos del usuario validados con UserCreate
        
    Returns:
        tuple: (success: bool, message: str, user_id: Optional[int])
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos", None

    try:
        # Validar los datos usando Pydantic
        validated_user = UserCreate(**user_data.dict()) if hasattr(user_data, 'dict') else user_data
        
        # Hash de la contraseña
        hashed_password = bcrypt.hashpw(
            validated_user.contrasena.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')

        with engine.connect() as connection:
            with connection.begin():
                # Verificar si ya existe el usuario por nombre_usuario, email o DNI
                check_query = text("""
                    SELECT COUNT(*) FROM usuarios 
                    WHERE nombre_usuario = :nombre_usuario 
                    OR email = :email
                    OR (dni IS NOT NULL AND dni = :dni)
                """)
                exists = connection.execute(
                    check_query, 
                    {
                        "nombre_usuario": validated_user.nombre_usuario,
                        "email": validated_user.email,
                        "dni": validated_user.dni
                    }
                ).scalar()
                
                if exists > 0:
                    return False, "Ya existe un usuario con este nombre de usuario, email o DNI", None
                
                # Insertar nuevo usuario
                query = text("""
                    INSERT INTO usuarios (nombre, apellido, nombre_usuario, email, dni, hash_contrasena, rol)
                    VALUES (:nombre, :apellido, :nombre_usuario, :email, :dni, :hash_contrasena, :rol) 
                    RETURNING id;
                """)
                result = connection.execute(query, {
                    "nombre": validated_user.nombre,
                    "apellido": validated_user.apellido,
                    "nombre_usuario": validated_user.nombre_usuario,
                    "email": validated_user.email,
                    "dni": validated_user.dni,
                    "hash_contrasena": hashed_password,
                    "rol": validated_user.rol
                }).scalar_one()
                
            logger.info("Usuario creado exitosamente", extra={
                'action': 'user_created', 
                'user_id': result, 
                'username': validated_user.nombre_usuario, 
                'role': validated_user.rol
            })
            return True, "Usuario creado exitosamente", result
            
    except ValidationError as error:
        error_msg = "Error de validación: " + "; ".join([f"{e['loc'][0]}: {e['msg']}" for e in error.errors()])
        logger.error(f"Error de validación al crear usuario: {error_msg}", extra={
            'action': 'user_validation_failed'
        })
        return False, error_msg, None
        
    except Exception as error:
        logger.error(f"Error al crear usuario: {str(error)}", extra={
            'action': 'user_creation_failed'
        })
        return False, f"Error interno: {str(error)}", None
        
    finally:
        if engine:
            engine.dispose()

def get_all_users() -> tuple[bool, str, List[User]]:
    """
    Obtiene todos los usuarios de la base de datos con validación Pydantic.
    
    Returns:
        tuple: (success: bool, message: str, users: List[User])
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos", []

    try:
        with engine.connect() as connection:
            query = text("""
                SELECT id, nombre, apellido, nombre_usuario, email, dni, hash_contrasena, 
                       rol, fecha_creacion 
                FROM usuarios 
                ORDER BY fecha_creacion DESC
            """)
            result = connection.execute(query)
            
            users = []
            for row in result:
                try:
                    user = User(
                        id=row[0],
                        nombre=row[1],
                        apellido=row[2],
                        nombre_usuario=row[3],
                        email=row[4],
                        dni=row[5],
                        hash_contrasena=row[6],
                        rol=row[7],
                        fecha_creacion=row[8]
                    )
                    users.append(user)
                except ValidationError as ve:
                    logger.warning(f"Usuario con ID {row[0]} tiene datos inválidos: {ve}")
                    continue
                    
            logger.info("Usuarios obtenidos exitosamente", extra={
                'action': 'get_users_success', 'count': len(users)
            })
            return True, "Usuarios obtenidos exitosamente", users
            
    except Exception as error:
        logger.error(f"Error al obtener lista de usuarios: {str(error)}", extra={
            'action': 'get_users_failed'
        })
        return False, f"Error interno: {str(error)}", []
        
    finally:
        if engine:
            engine.dispose()


def get_user_by_id(user_id: int) -> tuple[bool, str, Optional[User]]:
    """
    Obtiene un usuario específico por ID con validación Pydantic.
    
    Args:
        user_id: ID del usuario a buscar
        
    Returns:
        tuple: (success: bool, message: str, user: Optional[User])
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos", None

    try:
        with engine.connect() as connection:
            query = text("""
                SELECT id, nombre, apellido, nombre_usuario, email, dni, hash_contrasena, 
                       rol, fecha_creacion 
                FROM usuarios 
                WHERE id = :user_id
            """)
            result = connection.execute(query, {"user_id": user_id}).fetchone()
            
            if not result:
                return False, "Usuario no encontrado", None
            
            user = User(
                id=result[0],
                nombre=result[1],
                apellido=result[2],
                nombre_usuario=result[3],
                email=result[4],
                dni=result[5],
                hash_contrasena=result[6],
                rol=result[7],
                fecha_creacion=result[8]
            )
            
            return True, "Usuario encontrado", user
            
    except ValidationError as ve:
        logger.error(f"Error de validación para usuario ID {user_id}: {ve}")
        return False, "Datos del usuario son inválidos", None
        
    except Exception as error:
        logger.error(f"Error al obtener usuario {user_id}: {str(error)}", extra={
            'action': 'get_user_failed', 'user_id': user_id
        })
        return False, f"Error interno: {str(error)}", None
        
    finally:
        if engine:
            engine.dispose()


def update_user(user_id: int, user_data: UserUpdate) -> tuple[bool, str, Optional[User]]:
    """
    Actualiza un usuario existente usando validación Pydantic.
    
    Args:
        user_id: ID del usuario a actualizar
        user_data: Datos de actualización validados con UserUpdate
        
    Returns:
        tuple: (success: bool, message: str, updated_user: Optional[User])
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos", None

    try:
        # Validar los datos usando Pydantic
        validated_data = UserUpdate(**user_data.dict()) if hasattr(user_data, 'dict') else user_data
        
        # Crear diccionario solo con campos que no son None
        update_fields = {k: v for k, v in validated_data.dict().items() if v is not None}
        
        if not update_fields:
            return False, "No hay campos para actualizar", None

        with engine.connect() as connection:
            with connection.begin():
                # Verificar que el usuario existe
                check_query = text("SELECT COUNT(*) FROM usuarios WHERE id = :user_id")
                exists = connection.execute(check_query, {"user_id": user_id}).scalar()
                
                if exists == 0:
                    return False, "Usuario no encontrado", None
                
                # Si se actualiza nombre_usuario o email, verificar que no existan
                if 'nombre_usuario' in update_fields:
                    username_check = text("""
                        SELECT COUNT(*) FROM usuarios 
                        WHERE nombre_usuario = :nombre_usuario AND id != :user_id
                    """)
                    username_exists = connection.execute(username_check, {
                        "nombre_usuario": update_fields['nombre_usuario'],
                        "user_id": user_id
                    }).scalar()
                    
                    if username_exists > 0:
                        return False, "Ya existe un usuario con este nombre de usuario", None
                
                if 'email' in update_fields:
                    email_check = text("""
                        SELECT COUNT(*) FROM usuarios 
                        WHERE email = :email AND id != :user_id
                    """)
                    email_exists = connection.execute(email_check, {
                        "email": update_fields['email'],
                        "user_id": user_id
                    }).scalar()
                    
                    if email_exists > 0:
                        return False, "Ya existe un usuario con este email", None
                
                # Verificar DNI único si se está actualizando
                if 'dni' in update_fields and update_fields['dni'] is not None:
                    dni_check = text("""
                        SELECT COUNT(*) FROM usuarios 
                        WHERE dni = :dni AND id != :user_id
                    """)
                    dni_exists = connection.execute(dni_check, {
                        "dni": update_fields['dni'],
                        "user_id": user_id
                    }).scalar()
                    
                    if dni_exists > 0:
                        return False, "Ya existe un usuario con este DNI", None
                
                # Construir query dinámico
                set_clause = ", ".join([f"{field} = :{field}" for field in update_fields.keys()])
                query = text(f"""
                    UPDATE usuarios 
                    SET {set_clause}
                    WHERE id = :user_id
                """)
                
                # Ejecutar actualización
                update_params = {**update_fields, "user_id": user_id}
                connection.execute(query, update_params)
                
        # Obtener usuario actualizado
        success, message, updated_user = get_user_by_id(user_id)
        
        if success:
            logger.info("Usuario actualizado exitosamente", extra={
                'action': 'user_updated', 'user_id': user_id, 'fields': list(update_fields.keys())
            })
            return True, "Usuario actualizado exitosamente", updated_user
        else:
            return False, "Error al obtener usuario actualizado", None
            
    except ValidationError as error:
        error_msg = "Error de validación: " + "; ".join([f"{e['loc'][0]}: {e['msg']}" for e in error.errors()])
        logger.error(f"Error de validación al actualizar usuario: {error_msg}", extra={
            'action': 'user_update_validation_failed', 'user_id': user_id
        })
        return False, error_msg, None
        
    except Exception as error:
        logger.error(f"Error al actualizar usuario {user_id}: {str(error)}", extra={
            'action': 'user_update_failed', 'user_id': user_id
        })
        return False, f"Error interno: {str(error)}", None
        
    finally:
        if engine:
            engine.dispose()


def delete_user(user_id: int) -> tuple[bool, str]:
    """
    Elimina un usuario de la base de datos.
    
    Args:
        user_id: ID del usuario a eliminar
        
    Returns:
        tuple: (success: bool, message: str)
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos"

    try:
        with engine.connect() as connection:
            with connection.begin():
                # Verificar que el usuario existe
                check_query = text("SELECT COUNT(*) FROM usuarios WHERE id = :user_id")
                exists = connection.execute(check_query, {"user_id": user_id}).scalar()
                
                if exists == 0:
                    return False, "Usuario no encontrado"
                
                # Eliminar usuario
                query = text("DELETE FROM usuarios WHERE id = :user_id")
                connection.execute(query, {"user_id": user_id})
                
        logger.info("Usuario eliminado exitosamente", extra={
            'action': 'user_deleted', 'user_id': user_id
        })
        return True, "Usuario eliminado exitosamente"
        
    except Exception as error:
        logger.error(f"Error al eliminar usuario {user_id}: {str(error)}", extra={
            'action': 'user_delete_failed', 'user_id': user_id
        })
        return False, f"Error interno: {str(error)}"
        
    finally:
        if engine:
            engine.dispose()


def search_users(search_term: str = "", role_filter: str = "", status_filter: str = "") -> tuple[bool, str, List[User]]:
    """
    Busca usuarios con filtros opcionales.
    
    Args:
        search_term: Término de búsqueda (nombre, apellido o usuario)
        role_filter: Filtro por rol ('admin', 'usuario', 'supervisor')
        status_filter: Filtro por estado (por ahora solo activos)
        
    Returns:
        tuple: (success: bool, message: str, users: List[User])
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos", []

    try:
        with engine.connect() as connection:
            # Base query
            base_query = """
                SELECT id, nombre, apellido, nombre_usuario, email, dni, hash_contrasena, 
                       rol, fecha_creacion 
                FROM usuarios 
                WHERE 1=1
            """
            
            params = {}
            conditions = []
            
            # Filtro de búsqueda por texto
            if search_term.strip():
                conditions.append("""
                    (LOWER(nombre) LIKE LOWER(:search_term) 
                     OR LOWER(apellido) LIKE LOWER(:search_term)
                     OR LOWER(nombre_usuario) LIKE LOWER(:search_term))
                """)
                params["search_term"] = f"%{search_term.strip()}%"
            
            # Filtro por rol
            if role_filter and role_filter.lower() not in ['todos los roles', 'todos']:
                conditions.append("LOWER(rol) = LOWER(:role_filter)")
                params["role_filter"] = role_filter.strip()
            
            # Construir query final
            if conditions:
                base_query += " AND " + " AND ".join(conditions)
            
            base_query += " ORDER BY fecha_creacion DESC"
            
            query = text(base_query)
            result = connection.execute(query, params)
            
            users = []
            for row in result:
                try:
                    user = User(
                        id=row[0],
                        nombre=row[1],
                        apellido=row[2],
                        nombre_usuario=row[3],
                        email=row[4],
                        dni=row[5],
                        hash_contrasena=row[6],
                        rol=row[7],
                        fecha_creacion=row[8]
                    )
                    users.append(user)
                except ValidationError as ve:
                    logger.warning(f"Usuario con ID {row[0]} tiene datos inválidos: {ve}")
                    continue
                    
            logger.info("Búsqueda de usuarios completada", extra={
                'action': 'search_users_success', 
                'count': len(users),
                'search_term': search_term,
                'role_filter': role_filter
            })
            return True, f"Se encontraron {len(users)} usuarios", users
            
    except Exception as error:
        logger.error(f"Error en búsqueda de usuarios: {str(error)}", extra={
            'action': 'search_users_failed'
        })
        return False, f"Error interno: {str(error)}", []
        
    finally:
        if engine:
            engine.dispose()


def get_user_statistics() -> tuple[bool, str, dict]:
    """
    Obtiene estadísticas generales de usuarios.
    
    Returns:
        tuple: (success: bool, message: str, stats: dict)
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos", {}

    try:
        with engine.connect() as connection:
            # Query para estadísticas
            query = text("""
                SELECT 
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN rol = 'admin' THEN 1 END) as admin_count,
                    COUNT(CASE WHEN rol = 'supervisor' THEN 1 END) as supervisor_count,
                    COUNT(CASE WHEN rol = 'usuario' THEN 1 END) as user_count
                FROM usuarios
            """)
            
            result = connection.execute(query).fetchone()
            
            stats = {
                "total_usuarios": result[0],
                "activos": result[0],  # Por ahora todos son activos
                "administradores": result[1],
                "supervisores": result[2], 
                "usuarios": result[3]
            }
            
            return True, "Estadísticas obtenidas exitosamente", stats
            
    except Exception as error:
        logger.error(f"Error al obtener estadísticas: {str(error)}", extra={
            'action': 'get_user_stats_failed'
        })
        return False, f"Error interno: {str(error)}", {}
        
    finally:
        if engine:
            engine.dispose()


def verify_user(user_credential: str, contrasena: str) -> tuple[bool, str, Optional[User]]:
    """
    Verifica las credenciales de un usuario usando email O nombre de usuario.
    
    Args:
        user_credential: Email o nombre de usuario
        contrasena: Contraseña en texto plano
        
    Returns:
        tuple: (success: bool, message: str, user: Optional[User])
    """
    engine = get_db_engine()
    if engine is None:
        return False, "Error de conexión a la base de datos", None

    try:
        with engine.connect() as connection:
            # Buscar por email O por nombre_usuario
            query = text("""
                SELECT id, nombre, apellido, nombre_usuario, email, dni, hash_contrasena, 
                       rol, fecha_creacion 
                FROM usuarios 
                WHERE email = :credential OR nombre_usuario = :credential
            """)
            result = connection.execute(query, {"credential": user_credential.strip().lower()}).fetchone()

            if result:
                stored_hash = result[6]
                if bcrypt.checkpw(contrasena.encode('utf-8'), stored_hash.encode('utf-8')):
                    user = User(
                        id=result[0],
                        nombre=result[1],
                        apellido=result[2],
                        nombre_usuario=result[3],
                        email=result[4],
                        dni=result[5],
                        hash_contrasena=result[6],
                        rol=result[7],
                        fecha_creacion=result[8]
                    )
                    
                    # Determinar tipo de credencial para logging
                    credential_type = "email" if "@" in user_credential else "username"
                    log_security_event(
                        logger, 
                        'login_success', 
                        f'Autenticación exitosa con {credential_type}', 
                        f'user_id:{user.id};credential_type:{credential_type}'
                    )
                    return True, "Autenticación exitosa", user
            
            # Log de intento de autenticación fallido (evento de seguridad)
            credential_type = "email" if "@" in user_credential else "username"
            log_security_event(
                logger, 
                'login_failed', 
                f'Credenciales incorrectas ({credential_type})', 
                f'credential_len:{len(user_credential)};credential_type:{credential_type}'
            )
            return False, "Usuario o contraseña incorrectos", None
            
    except ValidationError as ve:
        logger.error(f"Error de validación en autenticación: {ve}")
        return False, "Error de datos de usuario", None
        
    except Exception as error:
        logger.error(f"Error en verificación de usuario: {str(error)}", extra={
            'action': 'auth_error', 'credential_len': len(user_credential)
        })
        return False, "Error interno de autenticación", None
        
    finally:
        if engine:
            engine.dispose()


# Funciones de compatibilidad con el código existente
def add_user(nombre: str, apellido: str, nombre_usuario: str, contrasena: str, rol: str = 'usuario', dni: int = None) -> int | None:
    """
    Función de compatibilidad. Usa la nueva función create_user internamente.
    
    DEPRECATED: Usar create_user() con modelos Pydantic en su lugar.
    """
    try:
        user_data = UserCreate(
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=nombre_usuario,
            contrasena=contrasena,
            dni=dni,
            rol=rol
        )
        success, message, user_id = create_user(user_data)
        return user_id if success else None
    except Exception:
        return None


# Mantener función verify_user con firma original para compatibilidad
def verify_user_legacy(nombre_usuario: str, contrasena: str) -> int | None:
    """
    Función legacy de verificación que solo retorna el ID.
    
    DEPRECATED: Usar verify_user() que retorna información completa.
    """
    success, message, user = verify_user(nombre_usuario, contrasena)
    return user.id if success and user else None
