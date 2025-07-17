import reflex as rx
from sia.styles.sizes import SizeLogo, SizeText, SizeButton, SizeSpace
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.colors import Color

from components.imagen_open import open_image

img = open_image(r"./assets/logo.png")

def name_app_wth_logo() -> rx.Component:
    return rx.box(
        rx.hstack(
                    rx.image(
                        src=img,
                        width=SizeLogo.MEDIUM.value,
                        height="auto",
                        border_radius="50%",
                        background_color="white",
                    ),
                    rx.text(
                        "SIA",
                        font_size=SizeText.X_LARGE.value,
                        font_family=FontFamily.INTER.value,
                        font_weight= FontWeight.MEDIUM.value,
                    ),
                    align_items="center",
                    margin_left=SizeSpace.SMALL.value,
                    padding=SizeSpace.SMALL.value,
                ),
    )