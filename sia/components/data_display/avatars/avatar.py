"""
Componente avatar: representación visual de usuario.
"""
from typing import Optional
import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText


def avatar(
    name: str = "",
    size: str = "32px",
    bg_color: str = "#1F1F1F",
    text_color: str = "white",
    **kwargs,
) -> rx.Component:
    """
    Componente de avatar de usuario.
    
    Args:
        name: Nombre del usuario (se usa la primera letra)
        size: Tamaño del avatar
        bg_color: Color de fondo
        text_color: Color del texto
        **kwargs: Propiedades adicionales
        
    Returns:
        rx.Component: Avatar del usuario
    """
    # Obtener primera letra del nombre
    initial = name[0].upper() if name else "U"
    
    return rx.box(
        rx.text(
            initial,
            color=text_color,
            font_weight=FontWeight.BOLD.value,
            text_align="center",
            font_size=SizeText.SMALL.value,
        ),
        bg=bg_color,
        border_radius="50%",
        width=size,
        height=size,
        display="flex",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
        **kwargs,
    )