"""
Componente toast individual del sistema SIA.

Este módulo implementa el componente toast individual que muestra
una notificación con icono, mensaje y botón de cerrar.
"""

import reflex as rx
from typing import Optional, Callable
from sia.styles.sizes import SizeIcon, SizeText
from sia.styles.border import BorderRadius
from ._types import ToastType, ToastConfig


def toast(
    message: str,
    toast_type: ToastType = ToastType.INFO,
    auto_dismiss: bool = True,
    dismiss_timeout: int = 4000,
    on_dismiss: Optional[Callable] = None,
    toast_id: Optional[str] = None,
) -> rx.Component:
    """
    Componente toast individual con animaciones y auto-dismiss.

    Args:
        message: Mensaje a mostrar en el toast
        toast_type: Tipo de toast (SUCCESS, ERROR, WARNING, INFO)
        auto_dismiss: Si debe cerrarse automáticamente
        dismiss_timeout: Tiempo en ms para auto-dismiss
        on_dismiss: Callback al cerrar el toast
        toast_id: ID único del toast

    Returns:
        rx.Component: Componente toast renderizado
    """

    # Use rx.cond to handle different toast types when coming from state variables
    return rx.cond(
        toast_type == ToastType.SUCCESS,
        _render_toast_with_config(message, ToastType.SUCCESS.value, on_dismiss),
        rx.cond(
            toast_type == ToastType.ERROR,
            _render_toast_with_config(message, ToastType.ERROR.value, on_dismiss),
            rx.cond(
                toast_type == ToastType.WARNING,
                _render_toast_with_config(message, ToastType.WARNING.value, on_dismiss),
                _render_toast_with_config(
                    message, ToastType.INFO.value, on_dismiss
                ),  # default to INFO
            ),
        ),
    )


def _render_toast_with_config(
    message: str, config: ToastConfig, on_dismiss: Optional[Callable] = None
) -> rx.Component:
    """
    Helper function to render toast with a specific configuration.

    Args:
        message: Message to display
        config: Toast configuration (ToastConfig instance)
        on_dismiss: Dismiss callback

    Returns:
        rx.Component: Rendered toast component
    """
    return rx.box(
        rx.flex(
            # Icono
            rx.icon(
                config.icon,
                size=SizeIcon.MEDIUM.value,
                color=config.icon_color,
                margin_right="12px",
            ),
            # Mensaje
            rx.text(
                message,
                color=config.text_color,
                font_size=SizeText.MEDIUM.value,
                font_weight="500",
                flex="1",
            ),
            # Botón dismiss
            rx.button(
                rx.icon("x", size=SizeIcon.SMALL.value, color=config.text_color),
                on_click=on_dismiss,
                variant="ghost",
                size="1",
                margin_left="8px",
                background="transparent",
                _hover={"background": "rgba(255, 255, 255, 0.1)", "opacity": "0.8"},
                style={"border": "none", "outline": "none"},
            ),
            align_items="center",
            width="100%",
        ),
        background=config.background_color,
        border=f"1px solid {config.border_color}",
        border_radius=BorderRadius.MEDIUM.value,
        padding="16px",
        margin_bottom="8px",
        min_width="320px",
        max_width="480px",
        box_shadow="0 4px 12px rgba(0, 0, 0, 0.15)",
        # Animaciones CSS
        transition="all 0.3s ease-in-out",
        transform="translateX(0)",
        opacity="1",
        class_name="toast-item",
        # Asegurar que los estilos no sean sobrescritos
        style={
            "background_color": config.background_color,
            "color": config.text_color,
            "border_color": config.border_color,
        },
    )
