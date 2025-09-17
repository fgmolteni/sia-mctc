import reflex as rx
from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.sizes import BorderRadius, SizeSpace, SizeText


def button_sin_fondo_icon(
    text: str, icon: str, url: str, color: str, hover_bg: str
):
    return rx.link(
        rx.button(
            rx.hstack(
                rx.icon(tag=icon, font_size=SizeText.SMALL.value),
                rx.text(
                    text,
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    width="100%",
                ),
                align="center",
                spacing="4",
            ),
            variant="ghost",
            color=color,
            width="100%",
            padding=SizeSpace.SMALL.value,
            cursor="pointer",
            justify_content="left",
            _hover={"bg": hover_bg, "color": ColorText.PRIMARY.value},
            padding_x=SizeSpace.MEDIUM.value,
        ),
        href=url,
        width="100%",
        padding_x=SizeSpace.MEDIUM.value,
    )


def button_icon_text_border(text: str, icon: str) -> rx.Component:
    return rx.button(
        rx.icon(tag=icon, size=16, color=ColorText.PRIMARY.value),
        rx.text(
            text,
            width="100%",
            # padding="10px 0px",
            border_radius=BorderRadius.SMALL.value,
            font_family=FontFamily.DEFAULT.value,
            font_weight=FontWeight.BOLD.value,
            font_size=SizeText.MEDIUM.value,
            # bg=Color.primary.value,
            color=ColorText.PRIMARY.value,
        ),
        border=f"1px solid {Color.secondary.value}",
        _hover={"bg": Color.primary.value},
        justify_content="center",
        align_items="center",
        spacing="2",
        background=Color.background.value,
    )
