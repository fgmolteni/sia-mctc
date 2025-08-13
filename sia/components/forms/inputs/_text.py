import reflex as rx


def form_input(
    label: str, placeholder: str, type: str, name: str, on_change=None, value=None
) -> rx.Component:
    return rx.vstack(
        rx.text(label, weight="bold"),
        rx.input(
            placeholder=placeholder,
            type=type,
            name=name,
            on_change=on_change,
            value=value,
            variant="surface",
            radius="large",
        ),
        align_items="start",
    )


def form_date_input(
    label: str, name: str, default_value: str = None
) -> rx.Component:
    return rx.vstack(
        rx.text(label),
        rx.input(type="date", name=name, default_value=default_value),
        align_items="start",
    )


def form_time_input(
    label: str, name: str, default_value: str = None
) -> rx.Component:
    return rx.vstack(
        rx.text(label),
        rx.input(type="time", name=name, default_value=default_value),
        align_items="start",
    )
