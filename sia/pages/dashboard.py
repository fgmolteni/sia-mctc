import reflex as rx

def dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Inicio", size="9"),
        rx.text("Bienvenido al inicio!"),
        spacing="5",
        align="start",
        width="100%",
    )