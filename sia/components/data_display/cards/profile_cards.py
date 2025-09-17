"""
Tarjetas específicas para perfiles de usuario.
"""
import reflex as rx
from typing import Optional
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeSpace, SizeText
from sia.styles.border import CommonBorders, BorderRadius


def card_profile(
    title: str,
    content: str,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    **kwargs,
) -> rx.Component:
    """
    Tarjeta básica de perfil de usuario.
    
    Args:
        title: Título principal
        content: Contenido de la tarjeta
        subtitle: Subtítulo opcional
        icon: Ícono opcional
        **kwargs: Propiedades adicionales
        
    Returns:
        rx.Component: Tarjeta de perfil
    """
    header_content = []
    
    if icon:
        header_content.append(
            rx.icon(
                icon,
                size=20,
                color=ColorText.GRAY_600.value,
            )
        )
    
    header_content.append(
        rx.vstack(
            rx.text(
                title,
                font_weight=FontWeight.BOLD.value,
                color=ColorText.GRAY_800.value,
            ),
            rx.cond(
                subtitle,
                rx.text(
                    subtitle,
                    font_size=SizeText.SMALL.value,
                    color=ColorText.GRAY_500.value,
                ),
            ),
            spacing="1",
            align="start",
        )
    )
    
    return rx.card(
        rx.vstack(
            # Header
            rx.hstack(
                *header_content,
                width="100%",
                align="center",
                spacing="3",
            ),
            # Content
            rx.text(
                content,
                color=ColorText.GRAY_700.value,
                line_height="1.5",
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


def info_card_profile(
    name: str,
    email: str,
    role: str,
    area: str = "Ministerio C&T",
    avatar_initial: str = "U",
    status: str = "Activo",
    **kwargs,
) -> rx.Component:
    """
    Tarjeta de información completa de perfil de usuario.
    
    Args:
        name: Nombre completo del usuario
        email: Email del usuario
        role: Rol del usuario
        area: Área de trabajo
        avatar_initial: Inicial para el avatar
        status: Estado del usuario
        **kwargs: Propiedades adicionales
        
    Returns:
        rx.Component: Tarjeta de información de perfil
    """
    # Configuración de colores por rol
    role_colors = {
        "Administrador": {"bg": "#DBEAFE", "color": "#2563EB"},
        "Supervisor": {"bg": "#E9D5FF", "color": "#9333EA"},
        "Usuario": {"bg": "#DCFCE7", "color": "#16A34A"},
    }
    
    role_config = role_colors.get(role, {"bg": "#F3F4F6", "color": "#6B7280"})
    
    # Configuración de colores por estado
    status_colors = {
        "Activo": {"color": "#16A34A", "bg": "#DCFCE7"},
        "Inactivo": {"color": "#6B7280", "bg": "#F3F4F6"},
    }
    
    status_config = status_colors.get(status, status_colors["Activo"])
    
    return rx.card(
        rx.vstack(
            # Header con avatar y nombre
            rx.hstack(
                # Avatar
                rx.box(
                    rx.text(
                        avatar_initial,
                        color="white",
                        font_weight=FontWeight.BOLD.value,
                        text_align="center",
                    ),
                    bg=Color.primary.value,
                    border_radius="50%",
                    width="48px",
                    height="48px",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                # Info básica
                rx.vstack(
                    rx.text(
                        name,
                        font_weight=FontWeight.BOLD.value,
                        font_size="1.1em",
                        color=ColorText.GRAY_800.value,
                    ),
                    rx.text(
                        email,
                        font_size=SizeText.SMALL.value,
                        color=ColorText.GRAY_500.value,
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                # Estado
                rx.box(
                    rx.text(
                        status,
                        font_size=SizeText.SMALL.value,
                        font_weight=FontWeight.MEDIUM.value,
                        color=status_config["color"],
                    ),
                    bg=status_config["bg"],
                    padding="4px 8px",
                    border_radius="6px",
                ),
                width="100%",
                align="center",
                spacing="3",
            ),
            # Información adicional
            rx.divider(),
            rx.vstack(
                rx.hstack(
                    rx.text("Rol:", font_weight=FontWeight.MEDIUM.value),
                    rx.box(
                        rx.text(
                            role,
                            font_size=SizeText.SMALL.value,
                            font_weight=FontWeight.MEDIUM.value,
                            color=role_config["color"],
                        ),
                        bg=role_config["bg"],
                        padding="2px 6px",
                        border_radius="4px",
                    ),
                    width="100%",
                    justify="space-between",
                    align="center",
                ),
                rx.hstack(
                    rx.text("Área:", font_weight=FontWeight.MEDIUM.value),
                    rx.text(
                        area,
                        color=ColorText.GRAY_600.value,
                    ),
                    width="100%",
                    justify="space-between",
                    align="center",
                ),
                width="100%",
                spacing="2",
                align="start",
            ),
            width="100%",
            spacing="4",
            align="start",
        ),
        padding=SizeSpace.LARGE.value,
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.SMALL.value,
        width="100%",
        **kwargs,
    )