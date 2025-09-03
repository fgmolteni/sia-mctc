import reflex as rx
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeText, SizeIcon, BorderRadius, SizeSpace
from sia.styles.colors import Color, ColorText
from sia.styles.border import CommonBorders

def stat_card(title: str, value: str, icon: str, icon_color: str = "white.400", **kwargs) -> rx.Component:
    """Componente de tarjeta de estadísticas reutilizable.
    
    Args:
        title: Título de la estadística
        value: Valor numérico o texto a mostrar
        icon: Nombre del icono de Reflex
        icon_color: Color del icono (opcional, por defecto "white.400")
    
    Returns:
        rx.Component: Tarjeta de estadística
    """
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(
                    title,
                    color=ColorText.GRAY_500.value,
                    font_size=SizeText.MEDIUM.value,
                    font_weight=FontWeight.MEDIUM.value
                ),
                rx.spacer(),
                rx.icon(
                    tag=icon,
                    size=SizeIcon.LARGE.value,
                    color=icon_color,
                    padding=SizeSpace.SMALL.value,
                    border_radius=BorderRadius.SMALL.value,
                ),
                align="start",
                width="100%",
                spacing="5",
            ),
            rx.spacer(),
            rx.heading(
                value,
                font_size=SizeText.X_LARGE.value,
                font_weight=FontWeight.BOLD.value,
                align="left",
                justify="end",
                width="100%"
            ),
            width="100%",
            align="start",
            spacing="3"
        ),
        width_min="250px",
        width="100%",
        height="120px",
        padding=SizeSpace.MEDIUM.value,
        **kwargs
    )

def info_card_profile(
    title: str,
    content: rx.Component,
    icon: str = None,
    badge_text: str = None,
    actions: list = None,
    show_header: bool = True,
    show_footer: bool = False,
    footer_text: str = None,
    footer_actions: list = None,
) -> rx.Component:
    """
    Componente de tarjeta de información reutilizable con header y footer opcionales.

    Args:
        title: Título principal de la tarjeta
        content: Contenido principal (rx.Component)
        icon: Ícono para el header (nombre del ícono)
        badge_text: Texto del badge/chip de estado
        actions: Lista de componentes de acción (botones/menús) para el header
        show_header: Flag para mostrar/ocultar header
        show_footer: Flag para mostrar/ocultar footer
        footer_text: Texto del footer (ej: metadatos)
        footer_actions: Lista de componentes de acción para el footer
    """

    # Header
    header_content = []
    if show_header:
        header_left = rx.hstack(
            rx.icon(icon, size=16, color="#3b82f6") if icon else rx.fragment(),
            rx.text(title, font_weight="600", font_size="1.1rem"),
            (
                rx.badge(
                    badge_text,
                    color=ColorText.PRIMARY.value,
                    bg=Color.admin_bg.value,
                    px="2",
                    py="1",
                    border_radius=BorderRadius.DEFAULT.value,
                    font_weight=FontWeight.MEDIUM.value,
                )
                if badge_text
                else rx.fragment()
            ),
            spacing="2",
            align="center",
        )

        header_right = (
            rx.hstack(*actions, spacing="2", align="center")
            if actions
            else rx.fragment()
        )

        header_content.append(
            rx.hstack(
                header_left,
                rx.spacer(),
                header_right,
                width="100%",
                align="center",
                justify="between",
                padding_bottom="3",
                border_bottom=CommonBorders.LIGHT_SOLID,
                margin_bottom="4",
            )
        )

    # Footer
    footer_content = []
    if show_footer:
        footer_left = (
            rx.text(
                footer_text,
                font_size="0.875rem",
                color=ColorText.GRAY_500.value,
            )
            if footer_text
            else rx.fragment()
        )

        footer_right = (
            rx.hstack(*footer_actions, spacing="2", align="center")
            if footer_actions
            else rx.fragment()
        )

        footer_content.append(
            rx.hstack(
                footer_left,
                rx.spacer(),
                footer_right,
                width="100%",
                align="center",
                justify="between",
                padding_top="3",
                border_top=CommonBorders.LIGHT_SOLID,
                margin_top="4",
            )
        )

    return rx.card(
        rx.vstack(
            *header_content,
            content,
            *footer_content,
            width="100%",
            align="start",
            spacing="0",
        ),
        width="100%",
        padding=SizeSpace.MEDIUM.value,
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.SMALL.value,
    )

def card_profile(
    title: str, value: str = "Valor", user_initials: str = "AU"
) -> rx.Component:
    """Componente de tarjeta de perfil simple.
    
    Args:
        title: Título de la tarjeta
        value: Valor a mostrar
        user_initials: Iniciales del usuario (opcional)
    
    Returns:
        rx.Component: Tarjeta de perfil
    """
    return rx.card(
        rx.hstack(
            # avatar_circle(user_initials),
            rx.vstack(
                rx.text(
                    title,
                    color=ColorText.GRAY_500.value,
                    font_size=SizeText.MEDIUM.value,
                    font_weight=FontWeight.MEDIUM.value,
                ),
                rx.text(
                    value,
                    color=ColorText.GRAY_800.value,
                    font_size=SizeText.X_LARGE.value,
                    font_weight=FontWeight.BOLD.value,
                ),
                align="start",
                spacing="1",
            ),
            align="center",
            spacing="3",
        ),
        width_min="250px",
        width="100%",
        height="120px",
        padding=SizeSpace.MEDIUM.value,
    )