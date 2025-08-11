import reflex as rx
from sia.styles.border import CommonBorders, BorderRadius
from sia.styles.sizes import SizeSpace

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