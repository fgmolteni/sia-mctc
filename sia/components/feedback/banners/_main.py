import reflex as rx
from sia.styles.colors import Color
from sia.styles.border import BorderRadius


def top_banner_gradient() -> rx.Component:
    return rx.box(
        rx.flex(
            rx.text(
                "Sistema Interno de Administración. ",
                rx.link(
                    "Consulte la documentación para más información.",
                    href="#",
                    underline="none",
                    display="inline",
                    underline_offset="2px",
                    color=Color.info.value,
                    opacity="0.95",
                ),
                align_items="center",
                justify_content="center",
                margin="auto",
                #spacing="3",
                weight="medium",
            ),
        ),
        align_items="center",
        justify_content="center",
        z_index="1",
        padding="1em",
        position="relative",
        #top="4em",
        border_radius=BorderRadius.MEDIUM.value,
        box_shadow="0 4px 32px 0 rgba(30,60,10,0.15)",
    )
