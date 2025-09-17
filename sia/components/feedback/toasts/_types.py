"""
Tipos y configuraciones para componentes toast del sistema SIA.

Este módulo define el enum ToastType y las configuraciones asociadas
para cada tipo de notificación toast.
"""

from enum import Enum
from dataclasses import dataclass


@dataclass
class ToastConfig:
    """
    Configuración de colores e iconos para un tipo de toast.

    Attributes:
        background_color: Color de fondo del toast
        text_color: Color del texto
        border_color: Color del borde
        icon: Nombre del icono a mostrar
        icon_color: Color del icono
    """

    background_color: str
    text_color: str
    border_color: str
    icon: str
    icon_color: str


class ToastType(Enum):
    """
    Tipos de notificaciones toast disponibles en el sistema SIA.

    Cada tipo incluye configuración completa de colores, iconos y estilos
    integrados con el sistema de diseño del proyecto.
    """

    SUCCESS = ToastConfig(
        background_color="#22C55E",  # Verde más oscuro para mejor contraste
        text_color="#FFFFFF",
        border_color="#16A34A",  # Borde ligeramente más oscuro
        icon="check",
        icon_color="#FFFFFF",
    )

    ERROR = ToastConfig(
        background_color="#DC2626",  # Rojo mejorado para mejor contraste
        text_color="#FFFFFF",
        border_color="#B91C1C",  # Borde más oscuro
        icon="x",
        icon_color="#FFFFFF",
    )

    WARNING = ToastConfig(
        background_color="#F59E0B",  # Naranja/amarillo oscuro para mejor contraste
        text_color="#FFFFFF",  # Cambio a texto blanco por mejor legibilidad
        border_color="#D97706",  # Borde más oscuro
        icon="triangle_alert",
        icon_color="#FFFFFF",
    )

    INFO = ToastConfig(
        background_color="#3B82F6",  # Azul más oscuro para mejor contraste
        text_color="#FFFFFF",
        border_color="#2563EB",  # Borde más oscuro
        icon="info",
        icon_color="#FFFFFF",
    )
