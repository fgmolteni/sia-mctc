"""
Componentes de badges mejorados para roles y estados.
"""
import reflex as rx
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText


def enhanced_role_badge(text: str, role: str = "default", show_icon: bool = True) -> rx.Component:
    """
    Badge mejorado para roles de usuario.
    
    Args:
        text: Texto del badge
        role: Tipo de rol (admin, supervisor, usuario, default)
        show_icon: Si mostrar ícono
        
    Returns:
        rx.Component: Badge de rol
    """
    role_config = {
        "admin": {
            "bg": "#DBEAFE",
            "color": "#2563EB", 
            "icon": "shield",
        },
        "supervisor": {
            "bg": "#E9D5FF",
            "color": "#9333EA",
            "icon": "user-cog",
        },
        "usuario": {
            "bg": "#DCFCE7",
            "color": "#16A34A",
            "icon": "user",
        },
        "default": {
            "bg": "#F3F4F6",
            "color": "#6B7280",
            "icon": "circle",
        },
    }
    
    config = role_config.get(role.lower(), role_config["default"])
    
    content = []
    if show_icon:
        content.append(
            rx.icon(
                config["icon"],
                size=12,
                color=config["color"],
            )
        )
    
    content.append(
        rx.text(
            text,
            font_size=SizeText.SMALL.value,
            font_weight=FontWeight.MEDIUM.value,
            color=config["color"],
        )
    )
    
    return rx.hstack(
        *content,
        bg=config["bg"],
        padding="4px 8px",
        border_radius="6px",
        spacing="1",
        align="center",
        display="inline-flex",
    )


def enhanced_status_badge(text: str, status: str = "default", show_icon: bool = True) -> rx.Component:
    """
    Badge mejorado para estados.
    
    Args:
        text: Texto del badge
        status: Tipo de estado (active, inactive, pending, default)
        show_icon: Si mostrar ícono con punto de estado
        
    Returns:
        rx.Component: Badge de estado
    """
    status_config = {
        "active": {
            "bg": "#DCFCE7",
            "color": "#16A34A",
            "dot_color": "#22C55E",
        },
        "inactive": {
            "bg": "#F3F4F6",
            "color": "#6B7280",
            "dot_color": "#9CA3AF",
        },
        "pending": {
            "bg": "#FEF3C7",
            "color": "#D97706",
            "dot_color": "#F59E0B",
        },
        "default": {
            "bg": "#F3F4F6",
            "color": "#6B7280",
            "dot_color": "#9CA3AF",
        },
    }
    
    config = status_config.get(status.lower(), status_config["default"])
    
    content = []
    if show_icon:
        content.append(
            rx.box(
                width="8px",
                height="8px",
                bg=config["dot_color"],
                border_radius="50%",
            )
        )
    
    content.append(
        rx.text(
            text,
            font_size=SizeText.SMALL.value,
            font_weight=FontWeight.MEDIUM.value,
            color=config["color"],
        )
    )
    
    return rx.hstack(
        *content,
        bg=config["bg"],
        padding="4px 8px",
        border_radius="6px",
        spacing="2",
        align="center",
        display="inline-flex",
    )