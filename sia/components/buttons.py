from fastapi import background
import reflex as rx

from sia.styles.colors import Color, ColorText
from sia.styles.fonts import FontFamily, FontWeight
from sia.styles.sizes import BorderRadius, SizeSpace, SizeText


def button_general(text: str) -> rx.Component:
    return rx.button(
        rx.text(
            text, size="3", color=ColorText.PRIMARY.value
        ),
        width="100%",
        bg=Color.primary.value,
    )


def button_curve(text: str) -> rx.Component:
    return rx.link(
        rx.button(

        )
    )


def button_redondo(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.button(
            rx.text(
                text,
                font_family=FontFamily.DEFAULT.value,
                font_weight=FontWeight.MEDIUM.value,
                color=ColorText.PRIMARY.value,
            ),
            variant="outline",
            # color_scheme= Color.info.value,
            border_radius=BorderRadius.DEFAULT.value,
            border=F"1px solid {ColorText.PRIMARY.value}",
            bg=Color.background.value,
            _hover={"bg": Color.primary.value, "color": ColorText.PRIMARY.value,
                    "border": f"1px solid {ColorText.SECONDARY.value}"},
            px="16px",
            py="8px",
            width="100%",
        ),
        href=url,
        padding=SizeSpace.SMALL.value,
        width="100%",
    )


def button_sin_fondo(text: str):
    return rx.link(
        rx.button(
            "Feedback",
            size="1",
            variant="ghost",
            color_scheme="gray",
            font_family=FontFamily.DEFAULT.value,
            font_weight="500",
            color="#9ca3af",
            bg="transparent",
            _hover={"bg": Color.background.value,
                    "color": ColorText.PRIMARY.value},
            px="16px",
            py="8px",
            font_size="14px",
            width="100%",
        ),
        width="100%",
    )


def button_sin_fondo_icon(text: str, icon: str, url: str, color: str, hover_bg: str):
    return rx.link(
        rx.button(
            rx.hstack(
                rx.icon(tag=icon,
                        font_size=SizeText.SMALL.value),
                rx.text(
                    text,
                    font_size=SizeText.SMALL.value,
                    font_weight=FontWeight.MEDIUM.value,
                    width="100%"),
                align="center",
                spacing="4",
            ),
            variant="ghost",
            color=color,
            width="100%",
            padding=SizeSpace.SMALL.value,
            cursor="pointer",
            justify_content="left",
            _hover={
                "bg": hover_bg,
                "color": ColorText.PRIMARY.value
            },
            padding_x=SizeSpace.MEDIUM.value,
        ),
        href=url,
        width="100%",
        padding_x=SizeSpace.MEDIUM.value
    )


def button_icon_text_border(text: str, icon: str) -> rx.Component:
    return rx.button(
        rx.icon(tag=icon, size=16, color=ColorText.PRIMARY.value),
        rx.text(text,
                width="100%",
                # padding="10px 0px",
                border_radius=BorderRadius.SMALL.value,
                font_family=FontFamily.DEFAULT.value,
                font_weight=FontWeight.BOLD.value,
                font_size=SizeText.MEDIUM.value,
                #bg=Color.primary.value,
                color=ColorText.PRIMARY.value,
                ),
        border=f"1px solid {Color.secondary.value}",
        _hover={"bg": Color.primary.value},
        justify_content="center",
        align_items="center",
        spacing="2",
        background=Color.background.value,
    ),
