import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.sizes import SizeText, SizeSpace, SizeIcon
from sia.styles.fonts import FontWeight
from sia.styles.border import BorderRadius, CommonBorders
from sia.components.avartar import avatar_circle

def info_card_profile(
    title: str,
    content: rx.Component,
    icon: str = None,
    badge_text: str = None,
    actions: list = None,
    show_header: bool = True,
    show_footer: bool = False,
    footer_text: str = None,
    footer_actions: list = None
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
            rx.badge(
                badge_text,
                color=ColorText.PRIMARY.value,
                bg=Color.admin_bg.value,
                px="2",
                py="1",
                border_radius=BorderRadius.DEFAULT.value,
                font_weight=FontWeight.MEDIUM.value,
            ) if badge_text else rx.fragment(),
            gap="3",
            align_items="center",
        )
        
        header_right = rx.hstack(
            *actions if actions else [],
            gap="2",
            align_items="center",
        )
        
        header_content = [
            rx.flex(
                header_left,
                rx.spacer(),
                header_right,
                align_items="center",
                width="100%",
                mb="4",
            )
        ]
    
    # Footer
    footer_content = []
    if show_footer:
        footer_left = rx.text(
            footer_text or "Información no disponible",
            color="gray.500",
            size="2",
        )
        
        footer_right = rx.hstack(
            *footer_actions if footer_actions else [],
            gap="2",
            align_items="center",
        )
        
        footer_content = [
            rx.divider(margin_y="4"),
            rx.flex(
                footer_left,
                rx.spacer(),
                footer_right,
                align_items="center",
                width="100%",
            )
        ]
    
    return rx.box(
        *header_content,
        content,
        *footer_content,
        background=Color.background.value,
        padding=SizeSpace.X_LARGE.value,
        margin=SizeSpace.MEDIUM.value,
        border_radius=BorderRadius.MEDIUM.value,
        box_shadow="0 1px 3px rgba(0, 0, 0, 0.1)",
        border=CommonBorders.LIGHT_SOLID,
        width="100%",
        _hover={"box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"},
    )

def card_profile(title: str, value: str = "Valor", user_initials: str = "AU") -> rx.Component:
    return rx.card(
        rx.hstack(
            avatar_circle(user_initials),
            rx.vstack(
                rx.text(
                    title,
                    color=ColorText.GRAY_500.value,
                    font_size=SizeText.MEDIUM.value,
                    font_weight=FontWeight.MEDIUM.value
                ),
                rx.text(
                    value,
                    color=ColorText.GRAY_800.value,
                    font_size=SizeText.X_LARGE.value,
                    font_weight=FontWeight.BOLD.value
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
        padding=SizeSpace.MEDIUM.value
    )
