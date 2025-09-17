import reflex as rx
from sia.styles.border import BorderRadius, CommonBorders
from sia.styles.colors import ColorText
from sia.styles.fonts import FontWeight
from sia.styles.sizes import SizeIcon, SizeSpace, SizeText


def page_header(
    title: str, subtitle: str, action_button: rx.Component = None, back_button: bool = False, redirect: str = None
) -> rx.Component:
    """
    Componente header reutilizable para páginas

    Args:
        title: Título principal del header
        subtitle: Subtítulo descriptivo
        action_button: Botón de acción opcional (ej: "+ Nuevo Usuario")
        back_button: Si mostrar el botón de volver atrás
    """
    return rx.vstack(
        # Header principal con título, subtítulo y botón
        rx.hstack(
            # Botón de volver (opcional)
            rx.button(
                rx.icon("arrow-left", size=SizeIcon.LARGE.value),
                background="transparent",
                color=ColorText.GRAY_500.value,
                _hover={"color": ColorText.GRAY_800.value},
                padding="2",
                on_click=rx.redirect(redirect),
            ) if back_button else rx.box(),
            # Contenido izquierdo: título y subtítulo
            rx.vstack(
                rx.heading(
                    title,
                    font_size=SizeText.X_LARGE.value,
                    font_weight=FontWeight.BOLD.value,
                    color=ColorText.GRAY_800.value,
                ),
                rx.text(
                    subtitle,
                    color=ColorText.GRAY_500.value,
                    font_size=SizeText.MEDIUM.value,
                ),
                align="start",
                spacing="1",
            ),
            # Espaciador para empujar el botón a la derecha
            rx.spacer(),
            # Botón de acción (opcional)
            action_button if action_button else rx.box(),
            width="100%",
            align="center",
        ),
        width="100%",
        padding_x=SizeSpace.MEDIUM.value,
        margin_top=SizeSpace.MEDIUM.value,
        margin_bottom=SizeSpace.SMALL.value,
        # bg="white",
        # border=CommonBorders.LIGHT_SOLID,
        # border_radius=BorderRadius.SMALL.value,
        spacing="8",
    )


def new_user_button() -> rx.Component:
    """Botón específico para crear nuevo usuario"""
    from sia.pages.usuarios import UserState
    
    return rx.button(
        rx.hstack(
            rx.icon("plus", size=SizeIcon.LARGE.value),
            rx.text("Nuevo Usuario", font_size=SizeText.MEDIUM.value),
            width="100%",
            padding=SizeSpace.MEDIUM.value,
            align="center",
            spacing="3",
        ),
        bg="black",
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.SMALL.value,
        color="white",
        _hover={"bg": "gray.800"},
        _active={"bg": "gray.700"},
        weight="medium",
        underline="none",
        on_click=UserState.show_create_user_modal,
    )


def header_profiles() -> rx.Component:
    """Header para la página de perfiles"""
    return page_header(
        title="Perfiles de Usuarios",
        subtitle="Administra y gestiona los perfiles de usuarios",
        #action_button=new_user_button(),
        back_button=True,
        redirect="/dashboard",
    )
