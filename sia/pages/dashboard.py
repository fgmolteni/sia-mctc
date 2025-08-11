import reflex as rx

def dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.text("Welcome to the dashboard!"),
        spacing="5",
        align="start",
        width="100%",
    )