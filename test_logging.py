#!/usr/bin/env python3
"""
Script de prueba para el sistema de logging centralizado de SIA
"""

import os
from components.logging import get_sia_logger, log_security_event

def test_basic_logging():
    """Prueba básica del sistema de logging"""
    print("=== Probando Sistema de Logging SIA ===\n")
    
    # Configurar entorno de desarrollo
    os.environ['SIA_ENV'] = 'development'
    
    # Crear loggers para diferentes módulos
    db_logger = get_sia_logger('database')
    pdf_logger = get_sia_logger('pdf')
    auth_logger = get_sia_logger('auth')
    
    print("1. Probando logs de información...")
    db_logger.info("Conexión a base de datos establecida", extra={
        'action': 'db_connection', 'status': 'success'
    })
    
    pdf_logger.info("Generando reporte PDF", extra={
        'action': 'pdf_generation', 'file_type': 'anticipo'
    })
    
    print("2. Probando logs de advertencia...")
    db_logger.warning("Conexión lenta a base de datos detectada", extra={
        'action': 'db_slow_query', 'duration_ms': 5000
    })
    
    print("3. Probando logs de error...")
    try:
        # Simular un error
        raise ValueError("Error simulado para prueba")
    except Exception as e:
        db_logger.error(f"Error en operación de base de datos: {str(e)}", extra={
            'action': 'db_operation_failed', 'table': 'usuarios'
        })
    
    print("4. Probando eventos de seguridad...")
    log_security_event(auth_logger, 'login_attempt', 'Intento de login desde IP desconocida', 'user_123')
    log_security_event(auth_logger, 'suspicious_activity', 'Múltiples intentos fallidos', 'user_456')
    
    print("5. Probando niveles DEBUG...")
    db_logger.debug("Query SQL ejecutada", extra={
        'action': 'sql_query', 'query_type': 'SELECT', 'table': 'agentes'
    })
    
    print("\n=== Pruebas Completadas ===")
    print("Revisa los siguientes archivos de log:")
    print("- logs/database.log")
    print("- logs/pdf.log") 
    print("- logs/auth.log")
    print("- logs/errors.log")
    print("- logs/security.log")

def test_module_integration():
    """Prueba la integración con módulos migrados"""
    print("\n=== Probando Integración con Módulos ===\n")
    
    try:
        # Importar módulos migrados
        from components.db_users import get_all_users
        from components.pdf_generator import create_pdf
        
        print("1. Probando módulo de usuarios...")
        users = get_all_users()
        print(f"Obtenidos {len(users)} usuarios")
        
        print("2. Probando generador de PDF...")
        test_content = [
            "=== REPORTE DE PRUEBA ===",
            "Este es un PDF de prueba para el sistema de logging",
            f"Generado el: {os.popen('date').read().strip()}",
            "Sistema: SIA - Logging Test"
        ]
        
        test_pdf_path = "logs/test_report.pdf"
        success = create_pdf(test_pdf_path, test_content)
        
        if success:
            print(f"PDF de prueba creado: {test_pdf_path}")
        else:
            print("Error al crear PDF de prueba")
            
    except Exception as e:
        print(f"Error en integración: {e}")

if __name__ == "__main__":
    test_basic_logging()
    test_module_integration()
    
    print("\n=== Instrucciones ===")
    print("1. Revisa los archivos de log generados")
    print("2. Verifica que los mensajes tengan el formato correcto")
    print("3. Confirma que los eventos de seguridad estén en security.log")
    print("4. Ejecuta: tail -f logs/database.log para monitoreo en tiempo real")