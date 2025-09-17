"""
Tarjetas de permisos para diferentes módulos del sistema.
"""
import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeSpace, SizeText
from sia.styles.border import CommonBorders, BorderRadius


def permission_card_base(
    title: str,
    icon: str,
    description: str,
    permission_level: str = "no_acceso",
    **kwargs,
) -> rx.Component:
    """
    Tarjeta base para permisos.
    
    Args:
        title: Título del permiso
        icon: Ícono del módulo
        description: Descripción del permiso
        permission_level: Nivel de permiso (no_acceso, ver, editar)
        **kwargs: Propiedades adicionales
        
    Returns:
        rx.Component: Tarjeta de permiso
    """
    # Configuración de colores por nivel de permiso
    permission_config = {
        "no_acceso": {
            "bg": "#FEF2F2",
            "border": "#FECACA",
            "color": "#DC2626",
            "text": "Sin acceso",
        },
        "ver": {
            "bg": "#FEF3C7",
            "border": "#FDE68A",
            "color": "#D97706",
            "text": "Solo lectura",
        },
        "editar": {
            "bg": "#DCFCE7",
            "border": "#BBF7D0",
            "color": "#16A34A",
            "text": "Completo",
        },
    }
    
    config = permission_config.get(permission_level, permission_config["no_acceso"])
    
    return rx.card(
        rx.vstack(
            # Header con ícono y título
            rx.hstack(
                rx.icon(
                    icon,
                    size=20,
                    color=config["color"],
                ),
                rx.text(
                    title,
                    font_weight=FontWeight.BOLD.value,
                    color=ColorText.GRAY_800.value,
                ),
                width="100%",
                align="center",
                spacing="3",
            ),
            # Descripción
            rx.text(
                description,
                font_size=SizeText.SMALL.value,
                color=ColorText.GRAY_500.value,
            ),
            # Badge de nivel de permiso
            rx.box(
                rx.text(
                    config["text"],
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    color=config["color"],
                ),
                bg=config["bg"],
                border=f"1px solid {config['border']}",
                padding="4px 8px",
                border_radius="6px",
                align_self="start",
            ),
            width="100%",
            spacing="3",
            align="start",
        ),
        padding=SizeSpace.MEDIUM.value,
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.SMALL.value,
        width="100%",
        **kwargs,
    )


def dashboard_permission_card(permission_level: str = "no_acceso", **kwargs) -> rx.Component:
    """Tarjeta de permisos para Dashboard."""
    return permission_card_base(
        title="Dashboard",
        icon="bar-chart-3",
        description="Acceso a métricas y estadísticas del sistema",
        permission_level=permission_level,
        **kwargs,
    )


def users_permission_card(permission_level: str = "no_acceso", **kwargs) -> rx.Component:
    """Tarjeta de permisos para Usuarios."""
    return permission_card_base(
        title="Gestión de Usuarios",
        icon="users",
        description="Crear, editar y eliminar usuarios del sistema",
        permission_level=permission_level,
        **kwargs,
    )


def reports_permission_card(permission_level: str = "no_acceso", **kwargs) -> rx.Component:
    """Tarjeta de permisos para Reportes."""
    return permission_card_base(
        title="Reportes y Análisis",
        icon="file-text",
        description="Generar y descargar reportes de viáticos",
        permission_level=permission_level,
        **kwargs,
    )


def vehicles_permission_card(permission_level: str = "no_acceso", **kwargs) -> rx.Component:
    """Tarjeta de permisos para Vehículos."""
    return permission_card_base(
        title="Gestión de Vehículos",
        icon="car",
        description="Administrar flota de vehículos oficiales",
        permission_level=permission_level,
        **kwargs,
    )