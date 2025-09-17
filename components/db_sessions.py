"""Funciones de base de datos para manejo de sesiones de usuario."""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import secrets
from sqlalchemy import text
from .db_common import get_db_engine
from .db_audit import log_user_action


def create_user_session(
    user_id: int,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    session_duration_hours: int = 24
) -> Optional[str]:
    """
    Crea una nueva sesión para un usuario.
    
    Args:
        user_id: ID del usuario
        ip_address: Dirección IP del usuario
        user_agent: User agent del navegador
        session_duration_hours: Duración de la sesión en horas
        
    Returns:
        Token de sesión si fue creada exitosamente, None en caso contrario
    """
    engine = get_db_engine()
    
    try:
        # Generar token de sesión único
        session_token = secrets.token_urlsafe(32)
        expiration_date = datetime.now() + timedelta(hours=session_duration_hours)
        
        with engine.begin() as connection:
            # Desactivar sesiones anteriores del usuario
            deactivate_query = text("""
                UPDATE sesiones_usuario 
                SET activa = false 
                WHERE usuario_id = :user_id AND activa = true
            """)
            
            connection.execute(deactivate_query, {"user_id": user_id})
            
            # Crear nueva sesión
            insert_query = text("""
                INSERT INTO sesiones_usuario (
                    usuario_id, token_sesion, ip_address, user_agent, fecha_expiracion
                ) VALUES (
                    :user_id, :token_sesion, :ip_address, :user_agent, :fecha_expiracion
                )
            """)
            
            connection.execute(insert_query, {
                "user_id": user_id,
                "token_sesion": session_token,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "fecha_expiracion": expiration_date
            })
            
            # Registrar en auditoría
            log_user_action(
                user_id=user_id,
                action="crear_sesion",
                module="auth",
                description="Nueva sesión creada",
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            return session_token
            
    except Exception as e:
        print(f"Error al crear sesión: {e}")
        return None


def validate_session(session_token: str) -> Optional[Dict[str, Any]]:
    """
    Valida un token de sesión y retorna información del usuario si es válida.
    
    Args:
        session_token: Token de sesión a validar
        
    Returns:
        Información del usuario si la sesión es válida, None en caso contrario
    """
    engine = get_db_engine()
    
    try:
        with engine.begin() as connection:
            query = text("""
                SELECT s.id as session_id, s.usuario_id, s.fecha_inicio, s.fecha_expiracion,
                       u.nombre, u.apellido, u.nombre_usuario, u.rol, u.activo
                FROM sesiones_usuario s
                INNER JOIN usuarios u ON s.usuario_id = u.id
                WHERE s.token_sesion = :session_token 
                AND s.activa = true 
                AND s.fecha_expiracion > NOW()
                AND u.activo = true
            """)
            
            result = connection.execute(query, {"session_token": session_token})
            session_data = result.fetchone()
            
            if session_data:
                # Actualizar último acceso
                update_query = text("""
                    UPDATE sesiones_usuario 
                    SET fecha_ultimo_acceso = NOW() 
                    WHERE token_sesion = :session_token
                """)
                
                connection.execute(update_query, {"session_token": session_token})
                
                return dict(session_data._mapping)
            
            return None
            
    except Exception as e:
        print(f"Error al validar sesión: {e}")
        return None


def invalidate_session(session_token: str, user_id: Optional[int] = None) -> bool:
    """
    Invalida una sesión específica.
    
    Args:
        session_token: Token de sesión a invalidar
        user_id: ID del usuario (opcional, para auditoría)
        
    Returns:
        True si la sesión fue invalidada, False en caso contrario
    """
    engine = get_db_engine()
    
    try:
        with engine.begin() as connection:
            query = text("""
                UPDATE sesiones_usuario 
                SET activa = false 
                WHERE token_sesion = :session_token
            """)
            
            result = connection.execute(query, {"session_token": session_token})
            
            if result.rowcount > 0 and user_id:
                # Registrar en auditoría
                log_user_action(
                    user_id=user_id,
                    action="cerrar_sesion",
                    module="auth",
                    description="Sesión cerrada manualmente"
                )
            
            return result.rowcount > 0
            
    except Exception as e:
        print(f"Error al invalidar sesión: {e}")
        return False


def invalidate_all_user_sessions(user_id: int) -> bool:
    """
    Invalida todas las sesiones activas de un usuario.
    
    Args:
        user_id: ID del usuario
        
    Returns:
        True si las sesiones fueron invalidadas, False en caso contrario
    """
    engine = get_db_engine()
    
    try:
        with engine.begin() as connection:
            query = text("""
                UPDATE sesiones_usuario 
                SET activa = false 
                WHERE usuario_id = :user_id AND activa = true
            """)
            
            result = connection.execute(query, {"user_id": user_id})
            
            # Registrar en auditoría
            log_user_action(
                user_id=user_id,
                action="cerrar_todas_sesiones",
                module="auth",
                description=f"Todas las sesiones del usuario fueron cerradas ({result.rowcount} sesiones)"
            )
            
            return result.rowcount > 0
            
    except Exception as e:
        print(f"Error al invalidar sesiones del usuario: {e}")
        return False


def get_active_sessions(user_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Obtiene las sesiones activas, opcionalmente filtradas por usuario.
    
    Args:
        user_id: ID del usuario (opcional)
        
    Returns:
        Lista de sesiones activas
    """
    engine = get_db_engine()
    
    where_clause = "WHERE s.activa = true AND s.fecha_expiracion > NOW()"
    params = {}
    
    if user_id:
        where_clause += " AND s.usuario_id = :user_id"
        params["user_id"] = user_id
    
    query = text(f"""
        SELECT s.id, s.usuario_id, s.ip_address, s.user_agent,
               s.fecha_inicio, s.fecha_ultimo_acceso, s.fecha_expiracion,
               u.nombre, u.apellido, u.nombre_usuario
        FROM sesiones_usuario s
        INNER JOIN usuarios u ON s.usuario_id = u.id
        {where_clause}
        ORDER BY s.fecha_ultimo_acceso DESC
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query, params)
        return [dict(row._mapping) for row in result]


def cleanup_expired_sessions() -> int:
    """
    Limpia las sesiones expiradas de la base de datos.
    
    Returns:
        Número de sesiones eliminadas
    """
    engine = get_db_engine()
    
    try:
        with engine.begin() as connection:
            # Marcar como inactivas las sesiones expiradas
            update_query = text("""
                UPDATE sesiones_usuario 
                SET activa = false 
                WHERE activa = true AND fecha_expiracion <= NOW()
            """)
            
            result = connection.execute(update_query)
            
            # Eliminar sesiones muy antiguas (más de 30 días)
            delete_query = text("""
                DELETE FROM sesiones_usuario 
                WHERE fecha_inicio < NOW() - INTERVAL '30 days'
            """)
            
            delete_result = connection.execute(delete_query)
            
            # Registrar en auditoría
            if result.rowcount > 0 or delete_result.rowcount > 0:
                log_user_action(
                    user_id=None,
                    action="limpiar_sesiones",
                    module="sistema",
                    description=f"Sesiones expiradas: {result.rowcount}, Sesiones eliminadas: {delete_result.rowcount}"
                )
            
            return result.rowcount + delete_result.rowcount
            
    except Exception as e:
        print(f"Error al limpiar sesiones: {e}")
        return 0


def get_session_statistics() -> Dict[str, Any]:
    """
    Obtiene estadísticas de sesiones del sistema.
    
    Returns:
        Diccionario con estadísticas de sesiones
    """
    engine = get_db_engine()
    
    query = text("""
        SELECT 
            COUNT(CASE WHEN activa = true AND fecha_expiracion > NOW() THEN 1 END) as sesiones_activas,
            COUNT(CASE WHEN activa = false OR fecha_expiracion <= NOW() THEN 1 END) as sesiones_inactivas,
            COUNT(DISTINCT usuario_id) as usuarios_con_sesiones,
            AVG(EXTRACT(EPOCH FROM (fecha_ultimo_acceso - fecha_inicio))/3600) as duracion_promedio_horas,
            MAX(fecha_ultimo_acceso) as ultima_actividad
        FROM sesiones_usuario
        WHERE fecha_inicio >= NOW() - INTERVAL '7 days'
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query)
        stats = dict(result.fetchone()._mapping)
        
        # Redondear duración promedio
        if stats['duracion_promedio_horas']:
            stats['duracion_promedio_horas'] = round(stats['duracion_promedio_horas'], 2)
        
        return stats