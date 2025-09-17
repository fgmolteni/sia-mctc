import reflex as rx
from sia.styles.border import BorderRadius, CommonBorders
from sia.styles.sizes import SizeSpace


def form_select(
    label: str,
    name: str,
    options,  # Puede ser list[str] o list[dict] 
    placeholder: str = "Seleccione una opción",
    on_change=None,
    value=None,
    required: bool = False,
) -> rx.Component:
    # Procesar opciones - solo extraer labels si son diccionarios (sin usar rx.cond con isinstance)
    if isinstance(options, list) and len(options) > 0 and isinstance(options[0], dict):
        select_options = [opt["label"] for opt in options]
    else:
        select_options = rx.cond(options, options, [])
    
    return rx.vstack(
        rx.text(label, weight="bold"),
        rx.select(
            select_options,
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


def select_component(
    placeholder: str = None, 
    options: list[str] = None, 
    value=None, 
    on_change=None, 
    **kwargs
) -> rx.Component:
    return rx.select(
        rx.cond(options, options, []),
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        border=CommonBorders.LIGHT_SOLID,
        border_radius=BorderRadius.SMALL.value,
        py=SizeSpace.SMALL.value,
        px=SizeSpace.SMALL.value,
        width="100%",
        **kwargs
    )
