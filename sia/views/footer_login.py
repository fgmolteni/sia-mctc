import reflex as rx
from sia.styles.colors import Color

def footer_login() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("© Ministerio de Ciencia y Tecnología - 2025", size="1", color=Color.accent.value),
            gap=1,
            align_items="start",
            opacity="0.5"
        ),
        width="100vw",
        position="fixed",
        bottom="0",
        left="0",
        padding="1em",
        background="transparent",
    )