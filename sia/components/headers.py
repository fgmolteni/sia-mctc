from fastapi import background
import reflex as rx
from sia.styles.sizes import BorderRadius, SizeLogo, SizeText, SizeButton, SizeSpace
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.colors import Color, ColorText

from components.imagen_open import open_image

img = open_image(r"./assets/logo.png")


def name_app_wth_logo() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(
                src=img,
                width=SizeLogo.MEDIUM.value,
                height=SizeLogo.MEDIUM.value,
                border_radius="50%",
                background_color="white",
            ),
            rx.text(
                "SIA",
                font_size=SizeText.X_LARGE.value,
                font_family=FontFamily.INTER.value,
                font_weight=FontWeight.MEDIUM.value,
            ),
            align_items="center",
            margin_left=SizeSpace.SMALL.value,
            padding=SizeSpace.SMALL.value,
        ),
    )


def only_isologo(theme: str) -> rx.Component:
    if theme=="Dark":
        background=Color.background.value
        text_color=ColorText.PRIMARY.value
    return rx.box(rx.hstack(
        rx.text(
            "S",
            font_family=FontFamily.SPACE_MONO.value,
            font_size=SizeText.X_LARGE.value,
            font_weight=FontWeight.BOLD.value,
            color=text_color,
        ),
        rx.text(
            "i",
            font_family=FontFamily.SPACE_MONO.value,
            font_size=SizeText.X_LARGE.value,
            font_weight=FontWeight.BOLD.value,
            font_style="italic",
            color=ColorText.ACCENT.value,

        ),
        rx.text(
            "A",
            font_family=FontFamily.SPACE_MONO.value,
            font_size=SizeText.X_LARGE.value,
            font_weight=FontWeight.BOLD.value,
            #color=ColorText.PRIMARY.value,
            # font_style="italic",
            color=text_color,

        ),
        spacing="0",
        align_items="center",
        margin_left=SizeSpace.SMALL.value,
        padding=SizeSpace.SMALL.value,

    ),
        align="center",
        background=background,
        border=BorderRadius.SMALL.value,
        padding=SizeSpace.SMALL.value,
    )
