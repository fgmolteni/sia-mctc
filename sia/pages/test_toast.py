"""
Página de prueba para toasts
"""

import reflex as rx
from sia.components.feedback.toasts import toast_container, ToastState


class TestToastState(rx.State):
    """Estado para probar toasts"""

    def test_success_toast(self):
        """Probar toast de éxito"""
        yield ToastState.show_success("¡Toast de éxito funcionando!")

    def test_error_toast(self):
        """Probar toast de error"""
        yield ToastState.show_error("Toast de error funcionando")

    def test_warning_toast(self):
        """Probar toast de warning"""
        yield ToastState.show_warning("Toast de advertencia funcionando")

    def test_info_toast(self):
        """Probar toast de info"""
        yield ToastState.show_info("Toast de información funcionando")


def test_toast_page() -> rx.Component:
    """Página de prueba para toasts"""
    return rx.box(
        rx.vstack(
            rx.heading("Prueba de Toasts", size="8"),
            rx.text("Haz clic en los botones para probar los toasts"),
            rx.hstack(
                rx.button(
                    "Toast Éxito",
                    on_click=TestToastState.test_success_toast,
                    color_scheme="green",
                    size="3",
                ),
                rx.button(
                    "Toast Error",
                    on_click=TestToastState.test_error_toast,
                    color_scheme="red",
                    size="3",
                ),
                rx.button(
                    "Toast Warning",
                    on_click=TestToastState.test_warning_toast,
                    color_scheme="yellow",
                    size="3",
                ),
                rx.button(
                    "Toast Info",
                    on_click=TestToastState.test_info_toast,
                    color_scheme="blue",
                    size="3",
                ),
                spacing="4",
            ),
            spacing="6",
            align="center",
            justify="center",
            min_height="50vh",
        ),
        # Contenedor de toasts
        toast_container(),
        width="100%",
        height="100vh",
    )
