import reflex as rx

from sia.styles.colors import Color, ColorText


def button_general(text: str) -> rx.Component:
    return rx.button(
        rx.text(
            text, size="3", color=ColorText.SECONDARY.value
        ),
        width="100%",
        background=Color.accent.value,
    )

def button_curve(text: str) -> rx.Component:
    return rx.link(
        rx.button(

        )
    )