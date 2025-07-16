from gettext import translation
from fastapi import background
import reflex as rx

from sia.styles.colors import Color

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
                    color = Color.accent.value,
                    opacity="0.95",
                    
                ),
                align_items=["start", "center"],
                margin="auto",
                spacing="3",
                weight="medium",
            ),
        ),
        z_index="1",
        padding="0.8em 2em",
        position="relative",
        top="4em",
        border_radius="1em",
        #box_shadow="0 4px 32px 0 rgba(30,60,10,0.15)",
        
    )
        