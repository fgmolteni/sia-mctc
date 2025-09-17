"""
Badges básicos para roles y estados.
"""
import reflex as rx
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText


def role_badge(text: str, role: str = "default") -> rx.Component:
    """
    Badge básico para roles de usuario.
    
    Args:
        text: Texto del badge
        role: Tipo de rol (admin, supervisor, usuario, default)
        
    Returns:
        rx.Component: Badge de rol
    """
    role_config = {
        "admin": {
            "bg": "#DBEAFE",
            "color": "#2563EB",
        },
        "supervisor": {
            "bg": "#E9D5FF",
            "color": "#9333EA",
        },
        "usuario": {
            "bg": "#DCFCE7",
            "color": "#16A34A",
        },
        "default": {
            "bg": "#F3F4F6",
            "color": "#6B7280",
        },
    }
    
    config = role_config.get(role.lower(), role_config["default"])
    
    return rx.box(
        rx.text(
            text,
            font_size=SizeText.SMALL.value,
            font_weight=FontWeight.MEDIUM.value,
            color=config["color"],
        ),
        bg=config["bg"],
        padding="4px 8px",
        border_radius="6px",
        display="inline-block",
    )


def status_badge(text: str, status: str = "default") -> rx.Component:
    """
    Badge básico para estados.
    
    Args:
        text: Texto del badge
        status: Tipo de estado (active, inactive, pending, default)
        
    Returns:
        rx.Component: Badge de estado
    """
    status_config = {
        "active": {
            "bg": "#DCFCE7",
            "color": "#16A34A",
        },
        "inactive": {
            "bg": "#F3F4F6",
            "color": "#6B7280",
        },
        "pending": {
            "bg": "#FEF3C7",
            "color": "#D97706",
        },
        "default": {
            "bg": "#F3F4F6",
            "color": "#6B7280",
        },
    }
    
    config = status_config.get(status.lower(), status_config["default"])
    
    return rx.box(
        rx.text(
            text,
            font_size=SizeText.SMALL.value,
            font_weight=FontWeight.MEDIUM.value,
            color=config["color"],
        ),
        bg=config["bg"],
        padding="4px 8px",
        border_radius="6px",
        display="inline-block",
    )