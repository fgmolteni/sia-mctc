"""
Contenedor de toasts del sistema SIA.

Este módulo implementa el contenedor principal que maneja
múltiples toasts con posicionamiento fijo.
"""

import reflex as rx
from ._toast import toast
from ._state import ToastState


def toast_container() -> rx.Component:
    """
    Contenedor para múltiples toasts con posicionamiento fijo.
    
    Renderiza todos los toasts activos en posición bottom-right
    con scroll automático si hay demasiados elementos.
    
    Returns:
        rx.Component: Contenedor de toasts
    """
    
    return rx.box(
        rx.foreach(
            ToastState.toasts,
            lambda toast_item: toast(
                message=toast_item.message,
                toast_type=toast_item.toast_type,
                auto_dismiss=toast_item.auto_dismiss,
                dismiss_timeout=toast_item.dismiss_timeout,
                on_dismiss=lambda: ToastState.dismiss_toast(toast_item.id),
                toast_id=toast_item.id
            )
        ),
        # Posicionamiento fijo en esquina inferior derecha
        position="fixed",
        bottom="20px",
        right="20px",
        z_index="999999",
        pointer_events="none",
        max_height="calc(100vh - 40px)",
        min_width="320px",
        max_width="480px",
        overflow="visible",
        display="flex",
        flex_direction="column",
        align_items="flex-end",
        gap="12px",
        # Permitir interacción solo en los toasts
        style={
            "& > *": {
                "pointer_events": "auto"
            }
        }
    )