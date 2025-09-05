"""
Componentes Toast para notificaciones del sistema SIA.

Este módulo proporciona un sistema completo de notificaciones toast que incluye:
- ToastType: Enum con tipos de notificación (success, error, warning, info)
- toast(): Componente toast individual
- toast_container(): Contenedor para múltiples toasts
- ToastState: Estado global para gestión de toasts

Ejemplo de uso:
    from sia.components.feedback.toasts import toast_container, ToastState
    
    # En el layout principal
    toast_container()
    
    # Para mostrar notificaciones
    ToastState.show_success("¡Operación exitosa!")
"""

from ._types import ToastType
from ._toast import toast
from ._container import toast_container
from ._state import ToastState, ToastItem

# Alias para compatibilidad con pruebas TDD
toast_component = toast

# Funciones de conveniencia globales
def show_toast_success(message: str):
    """Función global para mostrar toast de éxito"""
    return ToastState().show_success(message)

def show_toast_error(message: str):
    """Función global para mostrar toast de error"""
    return ToastState().show_error(message)

def show_toast_warning(message: str):
    """Función global para mostrar toast de advertencia"""
    return ToastState().show_warning(message)

def show_toast_info(message: str):
    """Función global para mostrar toast informativo"""
    return ToastState().show_info(message)

# API pública del módulo
__all__ = [
    "ToastType",
    "toast",
    "toast_component",
    "toast_container", 
    "ToastState",
    "ToastItem",
    "show_toast_success",
    "show_toast_error",
    "show_toast_warning",
    "show_toast_info"
]