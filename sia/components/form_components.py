import reflex as rx

def form_input(label: str, placeholder: str, type: str, name: str, on_change=None, value=None) -> rx.Component:
    return rx.vstack(
        rx.text(label),
        rx.input(placeholder=placeholder, type=type, name=name, on_change=on_change, value=value),
        align_items="start",
    )

def form_button(text: str, on_click=None) -> rx.Component:
    return rx.button(text, type_="submit", on_click=on_click)

def form_reset_button(text: str) -> rx.Component:
    return rx.button(text, type_="reset")

def form_date_input(label: str, name: str, default_value: str = None) -> rx.Component:
    return rx.vstack(
        rx.text(label),
        rx.input(type="date", name=name, default_value=default_value),
        align_items="start",
    )

def form_time_input(label: str, name: str, default_value: str = None) -> rx.Component:
    return rx.vstack(
        rx.text(label),
        rx.input(type="time", name=name, default_value=default_value),
        align_items="start",
    )

def form_select(label: str, name: str, options: list[str], placeholder: str = "Seleccione una opción", on_change=None, value=None) -> rx.Component:
    return rx.vstack(
        rx.text(label),
        rx.select(
            options,
            placeholder=placeholder,
            name=name,
            on_change=on_change,
            value=value,
            width="100%",
        ),
        align_items="start",
    )

