"""
Componente stat_card: tarjeta de estadística reutilizable.
"""
from typing import Optional
import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeSpace, SizeText
from sia.styles.border import CommonBorders, BorderRadius


def stat_card(
    title: str,
    value: str,
    icon: str,
    icon_color: str = "white",
    color_scheme: str = "blue",
    **kwargs,
) -> rx.Component:
    """
    Componente de tarjeta de estadística.
    
    Args:
        title: Título de la estadística
        value: Valor a mostrar
        icon: Nombre del ícono
        icon_color: Color del ícono (por defecto "white")
        color_scheme: Esquema de color (blue, green, purple, orange, red)
        **kwargs: Propiedades adicionales para el contenedor
        
    Returns:
        rx.Component: Tarjeta de estadística
    """
    # Mapeo de esquemas de color a colores específicos
    color_schemes = {
        "blue": {"bg": "#3B82F6", "text": "white"},
        "green": {"bg": "#10B981", "text": "white"},
        "purple": {"bg": "#8B5CF6", "text": "white"},
        "orange": {"bg": "#F59E0B", "text": "white"},
        "red": {"bg": "#EF4444", "text": "white"},
        "gray": {"bg": "#6B7280", "text": "white"},
    }
    
    colors = color_schemes.get(color_scheme, color_schemes["blue"])
    
    return rx.card(
        rx.vstack(
            # Header con título e ícono
            rx.hstack(
                rx.text(
                    title,
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    color=colors["text"],
                    opacity=0.9,
                ),
                rx.spacer(),
                rx.icon(
                    icon,
                    size=20,
                    color=icon_color,
                ),
                width="100%",
                align="center",
            ),
            # Valor principal
            rx.text(
                value,
                font_size="2em",
                font_weight=FontWeight.BOLD.value,
                color=colors["text"],
                line_height="1",
            ),
            width="100%",
            spacing="2",
            align="start",
        ),
        bg=colors["bg"],
        padding=SizeSpace.MEDIUM.value,
        border_radius=BorderRadius.SMALL.value,
        min_width="250px",
        width="100%",
        height="120px",
        **kwargs,
    )