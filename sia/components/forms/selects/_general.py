import reflex as rx
from sia.styles.border import BorderRadius, CommonBorders
from sia.styles.sizes import SizeSpace


def form_select(
    label: str,
    name: str,
    options: list[str],
    placeholder: str = "Seleccione una opción",
    on_change=None,
    value=None,
) -> rx.Component:
    return rx.vstack(
        rx.text(label, weight="bold"),
        rx.select(
            options,
            placeholder=placeholder,
            name=name,
            on_change=on_change,
            variant="surface",
            radius="large",
            value=value,
            width="100%",
        ),
        align_items="start",
    )


def select_component(placeholder: str, options: list[str]) -> rx.Component:
    return rx.select(
        options,
        placeholder=placeholder,
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.SMALL.value,
        py=SizeSpace.SMALL.value,
        px=SizeSpace.SMALL.value,
        width="100%",
    )
