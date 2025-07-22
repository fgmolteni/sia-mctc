import reflex as rx

def form_input(label: str, placeholder: str, type: str, name: str) -> rx.Component:
    return rx.vstack(
        rx.text(label),
        rx.input(placeholder=placeholder, type=type, name=name),
        align_items="start",
    )

def form_button(text: str) -> rx.Component:
    return rx.button(text, type_="submit")

def form_reset_button(text: str) -> rx.Component:
    return rx.button(text, type_="reset")
