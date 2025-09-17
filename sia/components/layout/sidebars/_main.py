"""
Átomos y moléculas básicas del sidebar siguiendo principios de Atomic Design.
Contiene los elementos fundamentales para construir la navegación lateral.
"""
import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontWeight, FontFamily
from sia.styles.sizes import SizeSpace, SizeIcon
from sia.styles.border import CommonBorders

from sia.components.branding import _logo

def sidebar_header() -> rx.Component:
    """
    Molécula del header del sidebar con logo y título.
    
    Returns:
        rx.Component: Header del sidebar con branding
    """
    return rx.box(
        _logo.name_app_wth_logo(),
        display="flex",
        align_items="center",
        justify_content="center", 
        padding=SizeSpace.MEDIUM.value,
        border_bottom=CommonBorders.LIGHT_SOLID,
        width="100%",
    )


def sidebar_section(title: str) -> rx.Component:
    """
    Átomo de título de sección en el sidebar.
    
    Args:
        title: Texto del título de la sección
        
    Returns:
        rx.Component: Título de sección estilizado
    """
    return rx.text(
        title,
        size="2",
        font_weight=FontWeight.MEDIUM.value,
        color=ColorText.GRAY_500.value,
        padding_top=SizeSpace.MEDIUM.value,
        padding_bottom=SizeSpace.SMALL.value,
        text_transform="uppercase",
        letter_spacing="0.05em",
    )


def sidebar_item(
    text: str,
    icon: str,
    href: str,
    is_active: bool = False,
    is_external: bool = False,
) -> rx.Component:
    """
    Átomo de elemento de navegación del sidebar.
    
    Args:
        text: Texto del ítem de navegación
        icon: Nombre del ícono (lucide)
        href: URL de destino
        is_active: Si el ítem está activo/seleccionado
        is_external: Si es un enlace externo
        
    Returns:
        rx.Component: Ítem de navegación completo
    """
    # Estilos base
    base_styles = {
        "width": "100%",
        "padding": SizeSpace.SMALL.value,
        "border_radius": "6px",
        "transition": "all 0.15s ease-in-out",
        "cursor": "pointer",
        "_hover": {
            "background_color": rx.color("gray", 2),
        },
    }
    
    # Estilos para ítem activo
    active_styles = {
        **base_styles,
        "background_color": rx.color("blue", 2),
        "color": rx.color("blue", 11),
        "_hover": {
            "background_color": rx.color("blue", 3),
        },
    }
    
    content = rx.hstack(
        rx.icon(
            icon,
            size=SizeIcon.SMALL.value,
            color=rx.color("blue", 11) if is_active else ColorText.GRAY_500.value,
        ),
        rx.text(
            text,
            font_weight=FontWeight.MEDIUM.value if is_active else FontWeight.NORMAL.value,
            color=rx.color("blue", 11) if is_active else ColorText.GRAY_700.value,
            size="2",
        ),
        spacing="2",
        align="center",
    )
    
    return rx.link(
        content,
        href=href,
        is_external=is_external,
        text_decoration="none",
        width="100%",
        style=active_styles if is_active else base_styles,
    )


def sidebar_sub_item(
    text: str,
    href: str,
    is_active: bool = False,
    is_external: bool = False,
) -> rx.Component:
    """
    Átomo de sub-elemento de navegación (indentado).
    
    Args:
        text: Texto del sub-ítem
        href: URL de destino
        is_active: Si el sub-ítem está activo
        is_external: Si es un enlace externo
        
    Returns:
        rx.Component: Sub-ítem de navegación
    """
    return rx.box(
        sidebar_item(text, "chevron-right", href, is_active, is_external),
        padding_left="1rem",
    )


def sidebar_collapsible_item(
    text: str,
    icon: str,
    children: list,
    is_expanded: bool = False,
) -> rx.Component:
    """
    Molécula de ítem colapsible con sub-ítems.
    
    Args:
        text: Texto del ítem principal
        icon: Ícono del ítem principal
        children: Lista de sub-ítems (componentes rx.Component)
        is_expanded: Si está expandido por defecto
        
    Returns:
        rx.Component: Ítem colapsible con sub-ítems
    """
    return rx.box(
        rx.button(
            rx.hstack(
                rx.icon(icon, size=SizeIcon.SMALL.value),
                rx.text(text, size="2"),
                rx.spacer(),
                rx.icon(
                    "chevron-down" if is_expanded else "chevron-right",
                    size=SizeIcon.SMALL.value,
                ),
                spacing="2",
                align="center",
                width="100%",
            ),
            variant="ghost",
            size="2",
            width="100%",
            justify="start",
        ),
        rx.cond(
            is_expanded,
            rx.vstack(
                *children,
                padding_left="1rem",
                spacing="1",
            ),
        ),
        width="100%",
    )


def sidebar_footer() -> rx.Component:
    """
    Molécula del footer del sidebar con información de usuario loggeado.
    Muestra información dinámica del usuario autenticado.
    
    Returns:
        rx.Component: Footer del sidebar con perfil de usuario dinámico
    """
    from sia.views.login_views import LoginState
    
    return rx.box(
        rx.hstack(
            rx.avatar(
                fallback=rx.cond(
                    LoginState.is_logged_in,
                    LoginState.avatar_initial,
                    "U"
                ),
                size="2",
                radius="full",
            ),
            rx.vstack(
                rx.text(
                    rx.cond(
                        LoginState.is_logged_in,
                        LoginState.user_name,
                        "Usuario SIA"
                    ),
                    font_weight=FontWeight.MEDIUM.value,
                    size="2",
                    color=ColorText.GRAY_700.value,
                ),
                rx.text(
                    rx.cond(
                        LoginState.is_logged_in,
                        rx.match(
                            LoginState.user_role,
                            ("admin", "Administrador - MCYT"),
                            ("supervisor", "Supervisor - MCYT"),
                            ("usuario", "Usuario - MCYT"),
                            "Usuario - MCYT",  # fallback por defecto
                        ),
                        "Ministerio C&T"
                    ),
                    size="1",
                    color=ColorText.GRAY_500.value,
                ),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("settings", size=SizeIcon.SMALL.value),
                variant="ghost",
                size="2",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        padding=SizeSpace.MEDIUM.value,
        border_top=CommonBorders.LIGHT_SOLID,
        width="100%",
    )