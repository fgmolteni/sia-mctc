from components.db_common import get_db_engine
from components.db_audit import log_user_action
from sqlalchemy import text
import uuid
from datetime import datetime, timedelta
from components.logging import get_sia_logger, log_security_event
from typing import List, Dict, Optional, Any

# Logger para este módulo
logger = get_sia_logger('permissions')

# =============================================================================
# FUNCIONES PARA GESTIONAR PERMISOS
# =============================================================================

def get_all_permissions() -> List[Dict[str, Any]]:
    """
    Obtiene todos los permisos disponibles en el sistema.
    
    Returns:
        List[Dict]: Lista de permisos con id, nombre, descripción y módulo.
    """
    engine = get_db_engine()
    if engine is None:
        logger.error("No se pudo conectar a la base de datos")
        return []

    try:
        with engine.connect() as connection:
            query = text("""
                SELECT id, nombre, descripcion, modulo, accion
                FROM permisos 
                ORDER BY modulo, nombre;
            """)
            result = connection.execute(query).fetchall()
            
            permissions = [{
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'modulo': row[3],
                'accion': row[4]
            } for row in result]
            
            logger.info(f"Se obtuvieron {len(permissions)} permisos", extra={
                'action': 'get_permissions_success',
                'count': len(permissions)
            })
            return permissions
            
    except Exception as error:
        logger.error(f"Error al obtener permisos: {str(error)}", extra={
            'action': 'get_permissions_failed'
        })
        return []
    finally:
        if engine:
            engine.dispose()

def get_user_permissions(user_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todos los permisos asignados a un usuario específico.
    
    Args:
        user_id (int): ID del usuario
        
    Returns:
        List[Dict]: Lista de permisos del usuario
    """
    engine = get_db_engine()
    if engine is None:
        return []

    try:
        with engine.connect() as connection:
            query = text("""
                SELECT p.id, p.nombre, p.descripcion, p.modulo, p.accion
                FROM permisos p
                INNER JOIN usuario_permisos up ON p.id = up.permiso_id
                WHERE up.usuario_id = :user_id
                ORDER BY p.modulo, p.nombre;
            """)
            result = connection.execute(query, {"user_id": user_id}).fetchall()
            
            permissions = [{
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'modulo': row[3],
                'accion': row[4]
            } for row in result]
            
            logger.info(f"Usuario {user_id} tiene {len(permissions)} permisos", extra={
                'action': 'get_user_permissions_success',
                'user_id': user_id,
                'permissions_count': len(permissions)
            })
            return permissions
            
    except Exception as error:
        logger.error(f"Error al obtener permisos del usuario {user_id}: {str(error)}", extra={
            'action': 'get_user_permissions_failed',
            'user_id': user_id
        })
        return []
    finally:
        if engine:
            engine.dispose()

def assign_permission_to_user(user_id: int, permission_id: int, assigned_by: int) -> bool:
    """
    Asigna un permiso específico a un usuario.
    
    Args:
        user_id (int): ID del usuario
        permission_id (int): ID del permiso
        assigned_by (int): ID del usuario que asigna el permiso
        
    Returns:
        bool: True si se asignó correctamente, False en caso contrario
    """
    engine = get_db_engine()
    if engine is None:
        return False

    try:
        with engine.connect() as connection:
            with connection.begin():
                # Verificar si el permiso ya está asignado
                check_query = text("""
                    SELECT COUNT(*) FROM usuario_permisos 
                    WHERE usuario_id = :user_id AND permiso_id = :permission_id;
                """)
                exists = connection.execute(check_query, {
                    "user_id": user_id,
                    "permission_id": permission_id
                }).scalar()
                
                if exists > 0:
                    logger.warning(f"Permiso {permission_id} ya asignado al usuario {user_id}", extra={
                        'action': 'assign_permission_duplicate',
                        'user_id': user_id,
                        'permission_id': permission_id
                    })
                    return False
                
                # Asignar el permiso
                insert_query = text("""
                    INSERT INTO usuario_permisos (usuario_id, permiso_id, otorgado_por_usuario_id)
                    VALUES (:user_id, :permission_id, :assigned_by);
                """)
                connection.execute(insert_query, {
                    "user_id": user_id,
                    "permission_id": permission_id,
                    "assigned_by": assigned_by
                })
                
                # Registrar en auditoría
                log_user_action(
                    user_id=assigned_by,
                    action="assign_permission",
                    module="permissions",
                    description=f"Asignó permiso {permission_id} al usuario {user_id}"
                )
                
                logger.info(f"Permiso {permission_id} asignado al usuario {user_id}", extra={
                    'action': 'assign_permission_success',
                    'user_id': user_id,
                    'permission_id': permission_id,
                    'assigned_by': assigned_by
                })
                return True
                
    except Exception as error:
        logger.error(f"Error al asignar permiso: {str(error)}", extra={
            'action': 'assign_permission_failed',
            'user_id': user_id,
            'permission_id': permission_id
        })
        return False
    finally:
        if engine:
            engine.dispose()

def remove_permission_from_user(user_id: int, permission_id: int, removed_by: int) -> bool:
    """
    Remueve un permiso específico de un usuario.
    
    Args:
        user_id (int): ID del usuario
        permission_id (int): ID del permiso
        removed_by (int): ID del usuario que remueve el permiso
        
    Returns:
        bool: True si se removió correctamente, False en caso contrario
    """
    engine = get_db_engine()
    if engine is None:
        return False

    try:
        with engine.connect() as connection:
            with connection.begin():
                delete_query = text("""
                    DELETE FROM usuario_permisos 
                    WHERE usuario_id = :user_id AND permiso_id = :permission_id;
                """)
                result = connection.execute(delete_query, {
                    "user_id": user_id,
                    "permission_id": permission_id
                })
                
                if result.rowcount == 0:
                    logger.warning(f"Permiso {permission_id} no encontrado para usuario {user_id}", extra={
                        'action': 'remove_permission_not_found',
                        'user_id': user_id,
                        'permission_id': permission_id
                    })
                    return False
                
                # Registrar en auditoría
                log_user_action(
                    user_id=removed_by,
                    action="remove_permission",
                    module="permissions",
                    description=f"Removió permiso {permission_id} del usuario {user_id}"
                )
                
                logger.info(f"Permiso {permission_id} removido del usuario {user_id}", extra={
                    'action': 'remove_permission_success',
                    'user_id': user_id,
                    'permission_id': permission_id,
                    'removed_by': removed_by
                })
                return True
                
    except Exception as error:
        logger.error(f"Error al remover permiso: {str(error)}", extra={
            'action': 'remove_permission_failed',
            'user_id': user_id,
            'permission_id': permission_id
        })
        return False
    finally:
        if engine:
            engine.dispose()

# =============================================================================
# FUNCIONES PARA GESTIONAR SESIONES
# =============================================================================

def create_user_session(user_id: int, ip_address: str = None) -> Optional[str]:
    """
    Crea una nueva sesión para un usuario.
    
    Args:
        user_id (int): ID del usuario
        ip_address (str): Dirección IP del usuario
        
    Returns:
        str: Token de sesión generado, None en caso de error
    """
    engine = get_db_engine()
    if engine is None:
        return None

    session_token = str(uuid.uuid4())
    expiry_time = datetime.now() + timedelta(hours=8)  # Sesión válida por 8 horas

    try:
        with engine.connect() as connection:
            with connection.begin():
                query = text("""
                    INSERT INTO sesiones_usuario (usuario_id, token_sesion, ip_address, fecha_expiracion)
                    VALUES (:user_id, :session_token, :ip_address, :expiry_time)
                    RETURNING id;
                """)
                session_id = connection.execute(query, {
                    "user_id": user_id,
                    "session_token": session_token,
                    "ip_address": ip_address,
                    "expiry_time": expiry_time
                }).scalar_one()
                
                # Registrar en auditoría
                log_user_action(
                    user_id=user_id,
                    action="login",
                    module="sessions",
                    description=f"Sesión creada desde IP: {ip_address or 'unknown'}"
                )
                
                logger.info(f"Sesión creada para usuario {user_id}", extra={
                    'action': 'session_created',
                    'user_id': user_id,
                    'session_id': session_id,
                    'ip_address': ip_address
                })
                return session_token
                
    except Exception as error:
        logger.error(f"Error al crear sesión: {str(error)}", extra={
            'action': 'session_creation_failed',
            'user_id': user_id
        })
        return None
    finally:
        if engine:
            engine.dispose()

def validate_session(session_token: str) -> Optional[Dict[str, Any]]:
    """
    Valida si una sesión está activa y no ha expirado.
    
    Args:
        session_token (str): Token de sesión
        
    Returns:
        Dict: Información de la sesión si es válida, None en caso contrario
    """
    engine = get_db_engine()
    if engine is None:
        return None

    try:
        with engine.connect() as connection:
            query = text("""
                SELECT s.id, s.usuario_id, u.nombre_usuario, u.rol, s.fecha_inicio, s.fecha_expiracion
                FROM sesiones_usuario s
                INNER JOIN usuarios u ON s.usuario_id = u.id
                WHERE s.token_sesion = :session_token 
                AND s.activa = true 
                AND s.fecha_expiracion > NOW();
            """)
            result = connection.execute(query, {"session_token": session_token}).fetchone()
            
            if result:
                session_info = {
                    'session_id': result[0],
                    'user_id': result[1],
                    'username': result[2],
                    'role': result[3],
                    'created_at': result[4],
                    'expires_at': result[5]
                }
                
                # Actualizar último acceso
                update_query = text("""
                    UPDATE sesiones_usuario 
                    SET fecha_ultimo_acceso = NOW() 
                    WHERE token_sesion = :session_token;
                """)
                connection.execute(update_query, {"session_token": session_token})
                connection.commit()
                
                return session_info
            else:
                log_security_event(logger, 'invalid_session', 'Token de sesión inválido o expirado', f'token_len:{len(session_token)}')
                return None
                
    except Exception as error:
        logger.error(f"Error al validar sesión: {str(error)}", extra={
            'action': 'session_validation_failed'
        })
        return None
    finally:
        if engine:
            engine.dispose()

def close_session(session_token: str) -> bool:
    """
    Cierra una sesión activa.
    
    Args:
        session_token (str): Token de sesión
        
    Returns:
        bool: True si se cerró correctamente, False en caso contrario
    """
    engine = get_db_engine()
    if engine is None:
        return False

    try:
        with engine.connect() as connection:
            with connection.begin():
                # Obtener información de la sesión antes de cerrarla
                info_query = text("""
                    SELECT usuario_id FROM sesiones_usuario 
                    WHERE token_sesion = :session_token AND activa = true;
                """)
                user_result = connection.execute(info_query, {"session_token": session_token}).fetchone()
                
                if not user_result:
                    return False
                
                user_id = user_result[0]
                
                # Cerrar la sesión
                update_query = text("""
                    UPDATE sesiones_usuario 
                    SET activa = false
                    WHERE token_sesion = :session_token;
                """)
                result = connection.execute(update_query, {"session_token": session_token})
                
                if result.rowcount > 0:
                    # Registrar en auditoría
                    log_user_action(
                        user_id=user_id,
                        action="logout",
                        module="sessions",
                        description="Sesión cerrada manualmente"
                    )
                    
                    logger.info(f"Sesión cerrada para usuario {user_id}", extra={
                        'action': 'session_closed',
                        'user_id': user_id
                    })
                    return True
                
                return False
                
    except Exception as error:
        logger.error(f"Error al cerrar sesión: {str(error)}", extra={
            'action': 'session_close_failed'
        })
        return False
    finally:
        if engine:
            engine.dispose()

def cleanup_expired_sessions() -> int:
    """
    Limpia sesiones expiradas del sistema.
    
    Returns:
        int: Número de sesiones limpiadas
    """
    engine = get_db_engine()
    if engine is None:
        return 0

    try:
        with engine.connect() as connection:
            with connection.begin():
                query = text("""
                    UPDATE sesiones_usuario 
                    SET activa = false
                    WHERE activa = true AND fecha_expiracion < NOW();
                """)
                result = connection.execute(query)
                cleaned_count = result.rowcount
                
                logger.info(f"Se limpiaron {cleaned_count} sesiones expiradas", extra={
                    'action': 'sessions_cleanup',
                    'cleaned_count': cleaned_count
                })
                return cleaned_count
                
    except Exception as error:
        logger.error(f"Error al limpiar sesiones: {str(error)}", extra={
            'action': 'sessions_cleanup_failed'
        })
        return 0
    finally:
        if engine:
            engine.dispose()

# =============================================================================
# FUNCIONES PARA ESTADÍSTICAS
# =============================================================================

def get_system_statistics() -> Dict[str, Any]:
    """
    Obtiene estadísticas generales del sistema.
    
    Returns:
        Dict: Estadísticas del sistema
    """
    engine = get_db_engine()
    if engine is None:
        return {}

    try:
        with engine.connect() as connection:
            # Estadísticas de usuarios
            users_query = text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN activo = true THEN 1 END) as active,
                    COUNT(CASE WHEN rol = 'administrador' THEN 1 END) as administrators,
                    COUNT(CASE WHEN ultimo_acceso > NOW() - INTERVAL '24 hours' THEN 1 END) as recent_activity
                FROM usuarios;
            """)
            users_stats = connection.execute(users_query).fetchone()
            
            # Estadísticas de sesiones
            sessions_query = text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN activa = true THEN 1 END) as active,
                    COUNT(CASE WHEN fecha_inicio > NOW() - INTERVAL '24 hours' THEN 1 END) as today
                FROM sesiones_usuario;
            """)
            sessions_stats = connection.execute(sessions_query).fetchone()
            
            # Estadísticas de auditoría
            audit_query = text("""
                SELECT 
                    COUNT(*) as total_actions,
                    COUNT(CASE WHEN fecha_accion > NOW() - INTERVAL '24 hours' THEN 1 END) as today_actions,
                    COUNT(CASE WHEN accion = 'login' AND fecha_accion > NOW() - INTERVAL '24 hours' THEN 1 END) as today_logins
                FROM auditoria_usuarios;
            """)
            audit_stats = connection.execute(audit_query).fetchone()
            
            statistics = {
                'users': {
                    'total': users_stats[0] if users_stats else 0,
                    'active': users_stats[1] if users_stats else 0,
                    'administrators': users_stats[2] if users_stats else 0,
                    'recent_activity': users_stats[3] if users_stats else 0
                },
                'sessions': {
                    'total': sessions_stats[0] if sessions_stats else 0,
                    'active': sessions_stats[1] if sessions_stats else 0,
                    'today': sessions_stats[2] if sessions_stats else 0
                },
                'activity': {
                    'total_actions': audit_stats[0] if audit_stats else 0,
                    'today_actions': audit_stats[1] if audit_stats else 0,
                    'today_logins': audit_stats[2] if audit_stats else 0
                }
            }
            
            return statistics
            
    except Exception as error:
        logger.error(f"Error al obtener estadísticas: {str(error)}", extra={
            'action': 'get_statistics_failed'
        })
        return {}
    finally:
        if engine:
            engine.dispose()