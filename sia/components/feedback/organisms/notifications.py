import reflex as rx


def notifications() -> rx.Component:
    """Componente mejorado para mostrar mensajes de éxito y error."""
    # Importación tardía para evitar importación circular
    from sia.pages.usuarios import UserState
    
    return rx.vstack(
        # Mensaje de éxito
        rx.cond(
            UserState.success_message != "",
            rx.callout(
                rx.hstack(
                    rx.text(UserState.success_message),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=UserState.clear_messages,
                        variant="ghost",
                        size="1",
                    ),
                    width="100%",
                    align="center",
                ),
                icon="check_check",
                color_scheme="green",
                width="100%",
            ),
        ),
        # Mensaje de error
        rx.cond(
            UserState.error_message != "",
            rx.callout(
                rx.hstack(
                    rx.text(UserState.error_message),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=16),
                        on_click=UserState.clear_messages,
                        variant="ghost",
                        size="1",
                    ),
                    width="100%",
                    align="center",
                ),
                icon="triangle_alert",
                color_scheme="red",
                width="100%",
            ),
        ),
        # Indicador de carga
        rx.cond(
            UserState.is_loading,
            rx.callout(
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text("Procesando..."),
                    spacing="3",
                    align="center",
                ),
                icon="info",
                color_scheme="blue",
                width="100%",
            ),
        ),
        spacing="3",
        width="100%",
    )