"""
Componente avatar_circle: avatar circular específico.
"""
import reflex as rx
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText


def avatar_circle(
    name: str = "",
    size: str = "48px",
    bg_color: str = "#1F1F1F",
    text_color: str = "white",
    border_color: str = "transparent",
    border_width: str = "2px",
    **kwargs,
) -> rx.Component:
    """
    Componente de avatar circular con borde opcional.
    
    Args:
        name: Nombre del usuario (se usa la primera letra)
        size: Tamaño del avatar
        bg_color: Color de fondo
        text_color: Color del texto
        border_color: Color del borde
        border_width: Grosor del borde
        **kwargs: Propiedades adicionales
        
    Returns:
        rx.Component: Avatar circular del usuario
    """
    # Obtener primera letra del nombre usando rx.cond con slicing válido
    initial = rx.cond(
        name != "", 
        name[:1].upper(),
        "U"
    )
    
    # Calcular tamaño de fuente basado en el tamaño del avatar
    font_size_map = {
        "24px": "10px",
        "32px": "12px", 
        "40px": "16px",
        "48px": "18px",
        "56px": "20px",
        "64px": "24px",
    }
    
    font_size = font_size_map.get(size, SizeText.MEDIUM.value)
    
    return rx.box(
        rx.text(
            initial,
            color=text_color,
            font_weight=FontWeight.BOLD.value,
            text_align="center",
            font_size=font_size,
            line_height="1",
        ),
        bg=bg_color,
        border_radius="50%",
        border=f"{border_width} solid {border_color}",
        width=size,
        height=size,
        display="flex",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
        **kwargs,
    )