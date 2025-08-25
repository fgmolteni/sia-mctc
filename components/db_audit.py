"""Funciones de base de datos para auditoría y registro de actividades de usuario."""

from typing import List, Dict, Optional, Any
from datetime import datetime
import json
from sqlalchemy import text
from .db_common import get_db_engine


def log_user_action(
    user_id: Optional[int],
    action: str,
    module: str,
    description: Optional[str] = None,
    old_data: Optional[Dict[str, Any]] = None,
    new_data: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    result: str = "exitoso"
) -> bool:
    """
    Registra una acción de usuario en la tabla de auditoría.
    
    Args:
        user_id: ID del usuario que realizó la acción (puede ser None para acciones del sistema)
        action: Tipo de acción realizada
        module: Módulo donde se realizó la acción
        description: Descripción detallada de la acción
        old_data: Datos anteriores (para updates/deletes)
        new_data: Datos nuevos (para inserts/updates)
        ip_address: Dirección IP del usuario
        user_agent: User agent del navegador
        result: Resultado de la acción ('exitoso', 'fallido', 'bloqueado')
        
    Returns:
        True si el registro fue exitoso, False en caso contrario
    """
    engine = get_db_engine()
    
    try:
        with engine.begin() as connection:
            query = text("""
                INSERT INTO auditoria_usuarios (
                    usuario_id, accion, modulo, descripcion,
                    datos_anteriores, datos_nuevos, ip_address,
                    user_agent, resultado
                ) VALUES (
                    :user_id, :action, :module, :description,
                    :old_data, :new_data, :ip_address,
                    :user_agent, :result
                )
            """)
            
            connection.execute(query, {
                "user_id": user_id,
                "action": action,
                "module": module,
                "description": description,
                "old_data": json.dumps(old_data) if old_data else None,
                "new_data": json.dumps(new_data) if new_data else None,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "result": result
            })
            
            return True
            
    except Exception as e:
        print(f"Error al registrar auditoría: {e}")
        return False


def get_user_audit_log(
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    module: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Obtiene el registro de auditoría filtrado por parámetros.
    
    Args:
        user_id: Filtrar por ID de usuario específico
        action: Filtrar por tipo de acción
        module: Filtrar por módulo
        start_date: Fecha de inicio del rango
        end_date: Fecha de fin del rango
        limit: Número máximo de registros a retornar
        
    Returns:
        Lista de registros de auditoría
    """
    engine = get_db_engine()
    
    # Construir la consulta dinámicamente
    where_conditions = []
    params = {"limit": limit}
    
    if user_id is not None:
        where_conditions.append("a.usuario_id = :user_id")
        params["user_id"] = user_id
    
    if action:
        where_conditions.append("a.accion = :action")
        params["action"] = action
    
    if module:
        where_conditions.append("a.modulo = :module")
        params["module"] = module
    
    if start_date:
        where_conditions.append("a.fecha_accion >= :start_date")
        params["start_date"] = start_date
    
    if end_date:
        where_conditions.append("a.fecha_accion <= :end_date")
        params["end_date"] = end_date
    
    where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
    
    query = text(f"""
        SELECT a.id, a.usuario_id, a.accion, a.modulo, a.descripcion,
               a.datos_anteriores, a.datos_nuevos, a.ip_address,
               a.user_agent, a.resultado, a.fecha_accion,
               u.nombre, u.apellido, u.nombre_usuario
        FROM auditoria_usuarios a
        LEFT JOIN usuarios u ON a.usuario_id = u.id
        {where_clause}
        ORDER BY a.fecha_accion DESC
        LIMIT :limit
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query, params)
        audit_logs = []
        
        for row in result:
            row_dict = dict(row._mapping)
            
            # Parsear JSON de datos anteriores y nuevos
            if row_dict['datos_anteriores']:
                try:
                    row_dict['datos_anteriores'] = json.loads(row_dict['datos_anteriores'])
                except json.JSONDecodeError:
                    row_dict['datos_anteriores'] = None
            
            if row_dict['datos_nuevos']:
                try:
                    row_dict['datos_nuevos'] = json.loads(row_dict['datos_nuevos'])
                except json.JSONDecodeError:
                    row_dict['datos_nuevos'] = None
            
            audit_logs.append(row_dict)
        
        return audit_logs


def get_audit_statistics(days: int = 30) -> Dict[str, Any]:
    """
    Obtiene estadísticas de auditoría para los últimos N días.
    
    Args:
        days: Número de días hacia atrás para calcular estadísticas
        
    Returns:
        Diccionario con estadísticas de auditoría
    """
    engine = get_db_engine()
    
    query = text("""
        SELECT 
            COUNT(*) as total_acciones,
            COUNT(DISTINCT usuario_id) as usuarios_activos,
            COUNT(CASE WHEN resultado = 'exitoso' THEN 1 END) as acciones_exitosas,
            COUNT(CASE WHEN resultado = 'fallido' THEN 1 END) as acciones_fallidas,
            COUNT(CASE WHEN resultado = 'bloqueado' THEN 1 END) as acciones_bloqueadas,
            COUNT(CASE WHEN accion = 'login' THEN 1 END) as total_logins,
            COUNT(CASE WHEN accion = 'logout' THEN 1 END) as total_logouts
        FROM auditoria_usuarios
        WHERE fecha_accion >= NOW() - INTERVAL ':days days'
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query, {"days": days})
        stats = dict(result.fetchone()._mapping)
        
        # Calcular porcentajes
        total = stats['total_acciones']
        if total > 0:
            stats['porcentaje_exitoso'] = round((stats['acciones_exitosas'] / total) * 100, 2)
            stats['porcentaje_fallido'] = round((stats['acciones_fallidas'] / total) * 100, 2)
            stats['porcentaje_bloqueado'] = round((stats['acciones_bloqueadas'] / total) * 100, 2)
        else:
            stats['porcentaje_exitoso'] = 0
            stats['porcentaje_fallido'] = 0
            stats['porcentaje_bloqueado'] = 0
        
        return stats


def get_most_active_users(days: int = 30, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Obtiene los usuarios más activos en los últimos N días.
    
    Args:
        days: Número de días hacia atrás
        limit: Número máximo de usuarios a retornar
        
    Returns:
        Lista de usuarios más activos con sus estadísticas
    """
    engine = get_db_engine()
    
    query = text("""
        SELECT 
            u.id, u.nombre, u.apellido, u.nombre_usuario,
            COUNT(a.id) as total_acciones,
            COUNT(CASE WHEN a.resultado = 'exitoso' THEN 1 END) as acciones_exitosas,
            COUNT(CASE WHEN a.resultado = 'fallido' THEN 1 END) as acciones_fallidas,
            MAX(a.fecha_accion) as ultima_actividad
        FROM usuarios u
        INNER JOIN auditoria_usuarios a ON u.id = a.usuario_id
        WHERE a.fecha_accion >= NOW() - INTERVAL ':days days'
        GROUP BY u.id, u.nombre, u.apellido, u.nombre_usuario
        ORDER BY total_acciones DESC
        LIMIT :limit
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query, {"days": days, "limit": limit})
        return [dict(row._mapping) for row in result]


def get_failed_login_attempts(hours: int = 24) -> List[Dict[str, Any]]:
    """
    Obtiene los intentos de login fallidos en las últimas N horas.
    
    Args:
        hours: Número de horas hacia atrás
        
    Returns:
        Lista de intentos de login fallidos
    """
    engine = get_db_engine()
    
    query = text("""
        SELECT 
            a.usuario_id, a.descripcion, a.ip_address, a.user_agent,
            a.fecha_accion, u.nombre_usuario
        FROM auditoria_usuarios a
        LEFT JOIN usuarios u ON a.usuario_id = u.id
        WHERE a.accion = 'login' 
        AND a.resultado = 'fallido'
        AND a.fecha_accion >= NOW() - INTERVAL ':hours hours'
        ORDER BY a.fecha_accion DESC
    """)
    
    with engine.connect() as connection:
        result = connection.execute(query, {"hours": hours})
        return [dict(row._mapping) for row in result]