import logging
import os
from datetime import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

class SIALogger:
    """Logger centralizado para el sistema SIA"""
    _instances = {}
    
    def __new__(cls, name):
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            cls._instances[name]._initialized = False
        return cls._instances[name]
    
    def __init__(self, name):
        if self._initialized:
            return
        
        self.logger = logging.getLogger(f"SIA.{name}")
        self.logger.setLevel(logging.DEBUG)
        
        # Crear directorio de logs si no existe
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Formateo personalizado con más información
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para archivo general con rotación
        file_handler = RotatingFileHandler(
            f"logs/{name}.log", 
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        
        # Handler para errores críticos
        error_handler = RotatingFileHandler(
            "logs/errors.log",
            maxBytes=10*1024*1024,  # 10MB 
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setFormatter(formatter)  
        error_handler.setLevel(logging.ERROR)
        
        # Handler para eventos de seguridad
        security_handler = RotatingFileHandler(
            "logs/security.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=10,  # Mantener más historial de seguridad
            encoding='utf-8'
        )
        security_handler.setFormatter(formatter)
        security_handler.setLevel(logging.WARNING)
        
        # Handler para consola (solo en desarrollo)
        if os.getenv('SIA_ENV', 'development') == 'development':
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(levelname)s | %(name)s | %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(console_handler)
        
        # Agregar todos los handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        
        # Handler de seguridad solo para módulos específicos
        if name in ['database', 'auth', 'users']:
            self.logger.addHandler(security_handler)
        
        self._initialized = True
    
    def get_logger(self):
        return self.logger

# Función helper para obtener logger fácilmente
def get_sia_logger(module_name):
    """
    Obtiene un logger para el módulo especificado
    
    Args:
        module_name: Nombre del módulo (ej: 'database', 'pdf', 'auth')
    
    Returns:
        Logger configurado para el módulo
    """
    return SIALogger(module_name).get_logger()

# Función para logging de eventos de seguridad
def log_security_event(logger, event_type, details, user_info=None):
    """
    Registra eventos de seguridad de manera consistente
    
    Args:
        logger: Logger a usar
        event_type: Tipo de evento (login, access_denied, etc.)
        details: Detalles del evento
        user_info: Información del usuario (sin datos sensibles)
    """
    security_msg = f"SECURITY_EVENT | {event_type} | {details}"
    if user_info:
        security_msg += f" | User: {user_info}"
    
    logger.warning(security_msg)