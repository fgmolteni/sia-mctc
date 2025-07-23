import reflex as rx
from sia.components.siderbar_componentes import sidebar_item, sidebar_items
from sia.components.ant_breadcrumb import breadcrumb, breadcrumb_item

from sia.components.buttons import button_sin_fondo_icon, button_icon_text_border

from sia.styles.colors import Color,ColorText
from sia.styles.fonts import FontFamily,FontWeight
from sia.styles.sizes import SizeSpace, SizeText, BorderRadius

def sidebar_main() -> rx.Component:
    return rx.box(
        rx.vstack(
            button_icon_text_border(text="Nuevo Documento", icon="plus"),
            rx.spacer(size=4),

            # Navigation Links
            rx.vstack(
                button_sin_fondo_icon("Buscar", "search", "#", color=ColorText.PRIMARY.value, hover_bg=Color.primary.value),
                button_sin_fondo_icon("Expedientes", "folder", "#", color=ColorText.PRIMARY.value, hover_bg=Color.primary.value),
                button_sin_fondo_icon("Recentes", "Clock", "#", color=ColorText.PRIMARY.value, hover_bg=Color.primary.value),
                button_sin_fondo_icon("Agentes", "users", "#", color=ColorText.PRIMARY.value, hover_bg=Color.primary.value),
                align="start",
                spacing="3",
                width="100%",
                margin_top=SizeSpace.SMALL.value,
            ),
            rx.spacer(),
            align="center",
            spacing="3",
            width="100%",
            padding_x="16px",  # Add horizontal padding here
        ),
        min_width="250px",
        height="calc(100vh - 60px)",
        position="fixed",
        left="0",
        top="60px",
        bg=Color.background.value,
        padding_y=SizeSpace.LARGE.value,
    )

            